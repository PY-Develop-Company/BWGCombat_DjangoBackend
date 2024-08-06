from django.http import JsonResponse, HttpResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Reward, Rank, PartnerSocialTasks, CompletedPartnersTasks, TaskTemplate
from user_app.models import UserData, UsersTasks, Fren, Link, LinkClick, TaskRoutes, User
from .utils import give_reward_to_inviter, check_if_link_is_telegram
from django.shortcuts import get_object_or_404, redirect
from levels_app.serializer import RankInfoSerializer, TasksSerializer
from rest_framework import status
from .serializer import SocialMediaTasksSerializer
from django.shortcuts import get_object_or_404
from .utils import place_items, claim_task_rewards
from django.utils.timezone import now
from django.db import transaction


def levels_home(request):
    return HttpResponse("levels home")


@api_view(["POST"])
@permission_classes([AllowAny])
def buy_task_view(request):
    task_id = request.data.get('taskId')

    user_task = UsersTasks.objects.get(id=task_id)
    userdata = UserData.objects.get(user_id=user_task.user.tg_id)

    if user_task.status in [UsersTasks.Status.CLAIMED, UsersTasks.Status.NOT_CLAIMED]:
        return JsonResponse({"message": "Task already done", "task_status": user_task.get_status_display()},
                            status=status.HTTP_200_OK)

    if user_task.status != UsersTasks.Status.IN_PROGRESS:
        return JsonResponse({"message": "Can't complete these task",
                             "task_status": user_task.get_status_display()}, status=status.HTTP_403_FORBIDDEN)

    if userdata.blocked_until > now():
        return JsonResponse({"message": "You can't buy tasks while prisoning",
                             "task_status": user_task.get_status_display()}, status=status.HTTP_403_FORBIDDEN)

    if user_task.task.template.price > userdata.gold_balance:
        return JsonResponse({"message": "You don't have enough money",
                             "task_status": user_task.get_status_display()}, status=status.HTTP_403_FORBIDDEN)

    done = False

    match user_task.task.template.task_type:
        case 1:
            link = Link.objects.get(task=TaskRoutes)
            if check_if_link_is_telegram(link):
                pass  # there will be subscription checking
            else:
                done = userdata.check_link_click()
        case 2:
            done = userdata.is_referrals_quantity_exceeds(user_task.completion_number)
        case _:
            userdata.gold_balance -= user_task.task.template.price
            userdata.save()
            done = True

    if done:
        if any(elem in [Reward.RewardType.JAIL, Reward.RewardType.GOLD] for elem in user_task.rewards.all()):
            rewards = user_task.rewards.all()
            claim_task_rewards(rewards, userdata, user_task)
            return JsonResponse({"message": "ok", "reward": f"{user_task.rewards.first().name}",
                                 "amount": f"{user_task.rewards.first().amount}",
                                 "task_status": user_task.get_status_display()})
        else:
            user_task.status = UsersTasks.Status.NOT_CLAIMED
            user_task.save()
            return JsonResponse({"message": "You completed the task. Now claim it",
                                 "task_status": user_task.get_status_display()}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": "You haven't completed the task or no checking for this task exists yet",
                             "task_status": user_task.get_status_display()})


@api_view(["POST"])
@permission_classes([AllowAny])
def claim_task_rewards_view(request):
    task_id = request.data.get('taskId')

    user_task = UsersTasks.objects.get(id=task_id)

    if user_task.status == UsersTasks.Status.CLAIMED:
        return JsonResponse({"message": "Task already claimed", "task_status": user_task.get_status_display()},
                            status=status.HTTP_200_OK)
    if user_task.status != UsersTasks.Status.NOT_CLAIMED:
        return JsonResponse({"message": "Can't claim these task", "task_status": user_task.get_status_display()},
                            status=status.HTTP_403_FORBIDDEN)

    userdata = UserData.objects.get(user_id=user_task.user.tg_id)

    rewards = user_task.rewards.all()
    claim_task_rewards(rewards, userdata, user_task)
    return JsonResponse({"message": "ok", "reward": f"{user_task.rewards.first().name}",
                         "amount": f"{user_task.rewards.first().amount}", "task_status": user_task.get_status_display()})


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def go_to_next_rank(request):
    user_id = request.data.get("userId")
    return go_to_next_rank_func(user_id)


def go_to_next_rank_func(user_id):
    userdata = get_object_or_404(UserData, user_id=user_id)

    current_rank = userdata.rank
    try:
        rank_to_go = current_rank.next_rank
    except Rank.DoesNotExist:
        return JsonResponse({"result": "no next rank exists"})

    if userdata.gold_balance >= current_rank.gold_required:
        place_items(userdata, rank_to_go)
        userdata.rank = rank_to_go
        userdata.max_energy_amount = rank_to_go.init_energy.amount
        userdata.multiclick_amount = rank_to_go.init_multiplier.amount
        userdata.energy_regeneration = rank_to_go.init_energy_regeneration
        userdata.current_stage = rank_to_go.init_stage
        initial = UsersTasks.objects.get(task=rank_to_go.init_stage.initial_task, user=userdata.user)
        initial.status = UsersTasks.Status.IN_PROGRESS

        initial.save()
        userdata.save()

        return JsonResponse({"result": "ok"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"result": "You don't have enough money to move on the next rank"},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def go_to_next_stage(request):
    user_id = request.data.get("userId")
    userdata = get_object_or_404(UserData, user_id=user_id)
    if userdata.current_stage.has_keylock and not userdata.has_key:
        return JsonResponse({"result": "You don't have key to go next stage"}, status=status.HTTP_403_FORBIDDEN)

    if userdata.current_stage.next_stage:
        userdata.current_stage = userdata.current_stage.next_stage
        return JsonResponse({"result": "ok"}, status=status.HTTP_200_OK)
    else:
        return go_to_next_rank_func(user_id)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_user_current_stage_info(request):
    user_id = request.data.get('userId')
    
    user_data = get_object_or_404(UserData, user_id=user_id)
    current_stage = user_data.current_stage
    stage_tasks = current_stage.tasks.values_list('id', flat=True)
    
    user_tasks = UsersTasks.objects.filter(user=user_data.user, task__in=stage_tasks).all()
    
    tasks_serializer = TasksSerializer(user_tasks, context={'user_id': user_data.user.tg_id}, many=True).data

    return JsonResponse({"stage_has_keylock": current_stage.has_keylock, "user_has_key": user_data.has_key, "tasks": tasks_serializer}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_social_media_tasks(request):
    user_id = request.data.get('userId')
    tasks = PartnerSocialTasks.objects.filter(is_partner=False)
    completed = CompletedPartnersTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)
    serializer = SocialMediaTasksSerializer(tasks, context={'completed_tasks': completed}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_partner_tasks(request):
    user_id = request.data.get('userId')
    tasks = PartnerSocialTasks.objects.filter(is_partner=True)
    completed = CompletedPartnersTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)
    serializer = SocialMediaTasksSerializer(tasks, context={'completed_tasks': completed}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def complete_partner_task(request):
    user_id = request.data.get('userId')
    task_id = request.data.get('taskId')
    
    task = PartnerSocialTasks.objects.get(id=task_id)
    user = UserData.objects.get(user=user_id)
    #check for completion
    completed = True

    if completed:
        if not CompletedPartnersTasks.objects.filter(task=task, user=user.user).exists():
            user.gold_balance += task.reward_amount
            CompletedPartnersTasks.objects.update_or_create(task=task, user=user.user)
            user.save()
    else:
        return JsonResponse({"result": "not ok"}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({"result": "ok"}, status=status.HTTP_200_OK)
