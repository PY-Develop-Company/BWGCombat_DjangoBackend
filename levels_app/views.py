from django.http import JsonResponse, HttpResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Reward, Rank, CompletedPartnersTasks, SocialTasks, CompletedSocialTasks, PartnersTasks
from user_app.models import UserData, UsersTasks, Fren, Link, LinkClick, TaskRoutes, User
from .utils import give_reward_to_inviter, check_if_link_is_telegram
from django.shortcuts import get_object_or_404, redirect
from levels_app.serializer import RankInfoSerializer, TasksSerializer
from rest_framework import status
from .serializer import SocialTasksSerializer, PartnersTasksSerializer
from django.shortcuts import get_object_or_404
from .utils import place_items
from django.utils.timezone import now
from django.db import transaction


def levels_home(request):
    return HttpResponse("levels home")


@api_view(["POST"])
@permission_classes([AllowAny])
def check_task_completion(request):
    task_id = request.data.get('taskId')
    task = UsersTasks.objects.get(id=task_id)
    userdata = UserData.objects.get(user_id=task.user.tg_id)

    if task.status != UsersTasks.Status.IN_PROGRESS:
        return JsonResponse({"message": "Can't complete these task"}, status=status.HTTP_403_FORBIDDEN)

    if task.status == UsersTasks.Status.COMPLETED:
        return JsonResponse({"message": "Task already done"}, status=status.HTTP_200_OK)

    if userdata.blocked_until > now():
        return JsonResponse({"message": "You can't buy tasks while prisoning"}, status=status.HTTP_403_FORBIDDEN)

    if task.task.template.price > userdata.gold_balance:
        return JsonResponse({"message": "You don't have enough money"}, status=status.HTTP_403_FORBIDDEN)

    done = False

    match task.task.template.task_type:
        case 1:
            link = Link.objects.get(task=TaskRoutes)
            if check_if_link_is_telegram(link):
                pass  # there will be subscription checking
            else:
                done = userdata.check_link_click()
        case 2:
            done = userdata.is_referrals_quantity_exceeds(task.completion_number)
        case _:
            userdata.gold_balance -= task.task.template.price
            done = True

    if done:
        rewards = task.rewards.all()
        for reward in rewards:
            userdata.receive_reward(reward)
        task.status = UsersTasks.Status.COMPLETED
        subtasks = task.get_user_subtasks(userdata.user)
        for ts in subtasks:
            ts.status = UsersTasks.Status.IN_PROGRESS
            ts.save()
        userdata.save()
        task.save()
        return JsonResponse({"message": "success", "reward": f"{task.rewards.first().name}", "amount": f"{task.rewards.first().amount}"})
    else:
        return JsonResponse({"message": "You haven't completed the task or no checking for this task exists yet"})


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
    
    tasks_serializer = TasksSerializer(user_tasks,context={'user_id':user_data.user.tg_id}, many=True).data

    return JsonResponse({"stage_has_keylock": current_stage.has_keylock, "user_has_key": user_data.has_key, "tasks": tasks_serializer}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_social_tasks(request):
    user_id = request.data.get('userId')
    user = User.objects.filter(tg_id=user_id).first()

    tasks = SocialTasks.objects.filter()
    completed = CompletedSocialTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)

    serializer = SocialTasksSerializer(tasks, context={'completed_tasks': completed, 'user_language': user.interface_lang.lang_code}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_partner_tasks(request):
    user_id = request.data.get('userId')
    user = User.objects.filter(tg_id=user_id).first()
    tasks = PartnersTasks.objects.all()
    completed = CompletedPartnersTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)

    serializer = PartnersTasksSerializer(tasks, context={'completed_tasks': completed, 'user_language': user.interface_lang.lang_code}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def complete_partner_task(request):
    user_id = request.data.get('userId')
    task_id = request.data.get('taskId')
    
    task = PartnersTasks.objects.get(id=task_id)
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


@api_view(["POST"])
def complete_social_task(request):
    user_id = request.data.get('userId')
    task_id = request.data.get('taskId')

    task = SocialTasks.objects.get(id=task_id)
    user = UserData.objects.get(user=user_id)
    # check for completion
    completed = True

    if completed:
        if not CompletedSocialTasks.objects.filter(task=task, user=user.user).exists():
            user.gold_balance += task.reward_amount
            CompletedSocialTasks.objects.update_or_create(task=task, user=user.user)
            user.save()
    else:
        return JsonResponse({"result": "not ok"}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({"result": "ok"}, status=status.HTTP_200_OK)
