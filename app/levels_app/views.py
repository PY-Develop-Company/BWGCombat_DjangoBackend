from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Task, Reward
from user_app.models import UserData, UsersTasks, Fren
from .utils import give_reward_to_inviter
from django.shortcuts import get_object_or_404, redirect
# from .models import Link, LinkClick


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
            done = userdata.check_link_click('https://t.me/justforcheckingone')
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
    give_reward_to_inviter(user_id)

    return JsonResponse({"result": "ok"})


#
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def get_task_info(request):
#     task_id = request.data.get("taskId")
#     task = get_object_or_404(Task, task_id=task_id)
#     return HttpResponse({task.text})
#

