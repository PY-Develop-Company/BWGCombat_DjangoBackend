from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Task, Reward
from user_app.models import UserData
from django.shortcuts import get_object_or_404


def levels_home(request):
    return HttpResponse("levels home")


def check_task_completion(user_data: UserData, reward: Reward):
    pass


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
