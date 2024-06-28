from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Task, Reward
from user_app.models import UserData
from django.shortcuts import get_object_or_404


def levels_home(request):
    return HttpResponse("levels home")


def add_reward(user_data: UserData, reward: Reward):
    reward_type = int(reward.reward_type)
    reward_amount = int(reward.amount)
    match reward_type:
        case 1:
            user_data.add_gold_coins(reward_amount)
        case 2:
            user_data.add_multiplier_coins(reward_amount)
        case 3:
            pass
        case _:
            return "No such type reward"


@api_view(["POST"])
@permission_classes([AllowAny])
def go_to_next_rank(request):
    user_id = request.data.get("userId")
    userdata = get_object_or_404(UserData, user_id=user_id)
    reward = userdata.rank_id.reward_id

    userdata.rank_id = userdata.rank_id.next_rank
    userdata.save()
    return JsonResponse({"result": "ok"})


@api_view(["POST"])
@permission_classes([AllowAny])
def request_task_submission(request):
    user_id = request.data.get("userId")
    task_id = request.data.get("taskId")
    userdata = get_object_or_404(UserData, user_id=user_id)
    task = get_object_or_404(Task, task_id=task_id)
    ### make some logic to check

    userdata.rank_id = userdata.rank_id.next_rank
    userdata.save()
    return JsonResponse({"result": "ok"})
