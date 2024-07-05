from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Task, Reward, Rank
from user_app.models import UserData, UsersTasks, Fren, Link, LinkClick
from .utils import give_reward_to_inviter, check_if_link_is_telegram
from django.shortcuts import get_object_or_404, redirect


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
        userdata.save()

        return JsonResponse({"result": "ok"})
    else:
        return JsonResponse({"result": "using go_to_next_rank() method when user's gold is not enough"})


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def go_to_next_stage(request):
#     user_id = request.data.get("userId")
#     # give_reward_to_inviter(user_id)
#
#     return JsonResponse({"result": "ok"})



