from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Task, Reward
from user_app.models import UserData, UsersTasks
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
    task = get_object_or_404(Task, id=task_id)
    ### make some logic to check
    
    task_done = UsersTasks.objects.create(user = userdata.user_id, task = task)
    task_done.save()

    current_tasks = userdata.stage_id.tasks_id.all()
    done_tasks = (UsersTasks.objects.filter(user = userdata.user_id, task__in=current_tasks))

    if len(current_tasks) == len(done_tasks):
        if userdata.stage_id.next_stage is not None:
            userdata.stage_id = userdata.stage_id.next_stage
        else:
            userdata.rank_id = userdata.rank_id.next_rank
            userdata.stage_id = userdata.rank_id.first_stage
    
    userdata.save()
    return JsonResponse({"result": "ok"})




