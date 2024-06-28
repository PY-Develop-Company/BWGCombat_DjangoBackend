from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Task, Reward
from user_app.models import UserData
from django.shortcuts import get_object_or_404


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
            pass
        case 2:
            done = userdata.check_referrals_quantity(10)
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
            userdata.receive_rewards(reward)
    else:
        return HttpResponse('You haven\'t completed the task or no checking for this task exists yet')


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
