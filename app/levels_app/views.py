from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Task, Reward, Rank, SocialMedia, CompletedSocialTasks
from user_app.models import UserData, UsersTask, Fren, Link, LinkClick
from .utils import give_reward_to_inviter, check_if_link_is_telegram
from django.shortcuts import get_object_or_404, redirect
from user_app.serializer import RankInfoSerializer
from rest_framework import status
from .serializer import SocialMediaTasksSerializer


def levels_home(request):
    return HttpResponse("levels home")


@api_view(["POST"])
@permission_classes([AllowAny])
def check_task_completion(user_id: int, task_id: int):
    task = Task.objects.get(id=task_id)
    userdata = UserData.objects.get(user_id=user_id)

    done = False

    match task.task_type:
        case 1:
            link = Link.objects.get(task=Task)
            if check_if_link_is_telegram(link):
                pass  # there will be subscription checking
            else:
                done = userdata.check_link_click()
        case 2:
            done = userdata.is_referrals_quantity_exceeds(task.completion_number)
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case _:
            return HttpResponse('No such task to check completion')

    # temporarily only checking frens quantity
    if done:
        rewards = task.rewards
        for reward in rewards:
            userdata.receive_reward(reward)
        # user_task = get_object_or_404(UsersTasks, user_id=user_id)
        # user_task.status = True
        # user_task.save()
    else:
        return HttpResponse('You haven\'t completed the task or no checking for this task exists yet')


@api_view(["POST"])
@permission_classes([AllowAny])
def go_to_next_rank(request):
    user_id = request.data.get("userId")
    userdata = UserData.objects.get(user_id=user_id)

    current_rank = userdata.rank
    try:
        rank_to_go = Rank.objects.get(id=current_rank.id+1)
    except Rank.DoesNotExist:
        return JsonResponse({"result": "no next rank exists"})

    if userdata.gold_balance >= rank_to_go.gold_required:
        give_reward_to_inviter(user_id)

        userdata.rank = rank_to_go
        userdata.max_energy_amount = rank_to_go.init_energy.amount
        userdata.multiclick_amount = rank_to_go.init_multiplier.amount
        userdata.save()

        return JsonResponse({"result": "ok"})
    else:
        return JsonResponse({"result": "using go_to_next_rank() method when user's gold is not enough"})


@api_view(["POST"])
@permission_classes([AllowAny])
def get_rank_info(request):
    user_id = request.data.get('userId')
    rank_id = request.data.get('rankId')

    user_data = get_object_or_404(UserData, user_id=user_id)
    rank_info = get_object_or_404(Rank, id=rank_id)
    if user_data.rank_id == rank_id:
        serializer = RankInfoSerializer(rank_info, context={'user_id': user_data.user_id_id})
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"rank_id": rank_info.id, "name": rank_info.name, 'description': rank_info.description}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_social_media_tasks(request):
    user_id = request.data.get('userId')
    tasks = SocialMedia.objects.filter(is_partner=False)
    completed = CompletedSocialTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)
    serializer = SocialMediaTasksSerializer(tasks, context={'completed_tasks': completed}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_partner_tasks(request):
    user_id = request.data.get('userId')
    tasks = SocialMedia.objects.filter(is_partner=True)
    completed = CompletedSocialTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)
    serializer = SocialMediaTasksSerializer(tasks, context={'completed_tasks': completed}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)
