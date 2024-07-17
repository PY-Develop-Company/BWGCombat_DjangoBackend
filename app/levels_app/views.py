from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Reward, Rank, SocialMedia, CompletedSocialTasks
from user_app.models import UserData, UsersTasks, Fren, Link, LinkClick, TaskRoutes
from .utils import give_reward_to_inviter, check_if_link_is_telegram
from django.shortcuts import get_object_or_404, redirect
from levels_app.serializer import RankInfoSerializer, ClosedRankSerializer
from rest_framework import status
from .serializer import SocialMediaTasksSerializer
from django.shortcuts import get_object_or_404
from .utils import place_items


def levels_home(request):
    return HttpResponse("levels home")


@api_view(["POST"])
@permission_classes([AllowAny])
def check_task_completion(request):
    task_id = request.data.get('taskId')
    task = UsersTasks.objects.get(id=task_id)
    userdata = UserData.objects.get(user_id=task.user.tg_id)


    if task.task.template.price > userdata.gold_balance:
        return JsonResponse({'message':'You don\'t have enough money'}, status=status.HTTP_403_FORBIDDEN)

    done = False
    print(userdata)

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
            task.status = UsersTasks.Status.COMPLETED
            done = True

    if done:
        rewards = task.rewards.all()
        for reward in rewards:
            userdata.receive_reward(reward)
            print(reward.__repr__())
            print(reward.reward_type)
        userdata.save()
        task.save()
        return JsonResponse({'message':'success'})
    else:
        return JsonResponse({"message":'You haven\'t completed the task or no checking for this task exists yet'})


@api_view(["POST"])
@permission_classes([AllowAny])
def go_to_next_rank(request):
    user_id = request.data.get("userId")
    userdata = get_object_or_404(UserData, user_id = user_id)

    current_rank = userdata.rank
    try:
        rank_to_go = current_rank.next_rank
    except Rank.DoesNotExist:
        return JsonResponse({"result": "no next rank exists"})

    if userdata.gold_balance >= rank_to_go.gold_required:
        place_items(userdata, rank_to_go)
        userdata.rank = rank_to_go
        userdata.max_energy_amount = rank_to_go.init_energy
        userdata.multiclick_amount = rank_to_go.init_multiplier
        userdata.energy_regeneration = rank_to_go.init_energy_regeneration
        userdata.save()

        return JsonResponse({"result": "ok"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"result": "You don't have enough money to move on the next rank"}, status=status.HTTP_403_FORBIDDEN)


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
        return JsonResponse(ClosedRankSerializer(rank_info).data, status=status.HTTP_200_OK)
    


@api_view(["POST"])
@permission_classes([AllowAny])
def buy_task(request):
    user_id = request.data.get('userId')
    task_id = request.data.get('taskId')



@api_view(["POST"])
def get_social_media_tasks(request):
    user_id = request.data.get('userId')
    tasks = SocialMedia.objects.filter(is_partner=False)
    completed = CompletedSocialTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)
    serializer = SocialMediaTasksSerializer(tasks, context={'completed_tasks': completed}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_partner_tasks(request):
    user_id = request.data.get('userId')
    tasks = SocialMedia.objects.filter(is_partner=True)
    completed = CompletedSocialTasks.objects.filter(user_id=user_id, task__in=tasks).values_list('id', flat=True)
    serializer = SocialMediaTasksSerializer(tasks, context={'completed_tasks': completed}, many=True)
    return JsonResponse({"tasks": serializer.data}, status=status.HTTP_200_OK)



