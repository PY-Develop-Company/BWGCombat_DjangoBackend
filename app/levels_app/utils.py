import asyncio
import random

from user_app.models import UserData, Fren, Link, UsersTasks
from .models import Rank, Stage, Reward, TaskRoutes
from django.shortcuts import get_object_or_404
from .models import Reward
from django.db.models import Q


# async def check_subscription(user_id):
#     chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
#     return False if chat_member.status in ['left', 'kicked'] else True
#
#
# def check_subscription_sync(user_id):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(check_subscription(user_id))


def give_reward_to_inviter(fren_id):
    try:
        inviter_id = Fren.objects.get(fren_id=fren_id)
    except Fren.DoesNotExist:
        return
    userdata = get_object_or_404(UserData, user_id=inviter_id)

    reward = userdata.rank.inviter_reward

    userdata.receive_reward(reward)
    userdata.save()


def check_if_link_is_telegram(link: Link):
    telegram_link_starts = ('t.me/', 'https://t.me/')
    index = link.url.find(telegram_link_starts[1])
    if index == -1:
        index = link.url.find(telegram_link_starts[0])
        return index != -1

    return True


def place_key(user_data: UserData, stage: Stage):
    avaliable_keys = list(stage.stage_template.task_with_keys.all())
    if not avaliable_keys: 
        return
    task = random.choice(avaliable_keys)
    key = UsersTasks.objects.create(user=user_data.user, task=task)
    key.rewards.add(Reward.objects.get(name="Key"))
    key.save()


def place_rewards_for_chests(user_data, chests:list[TaskRoutes]):
    for chest in chests:
        available_rewards = list(chest.template.rewards.exclude(Q(name='Key') | Q(name='Jail')))
        ts = UsersTasks.objects.create(user=user_data.user, task = chest)
        ts.rewards.add(random.choice(available_rewards))
        ts.save()


def place_another_tasks(user_data:UserData, tasks:list[TaskRoutes]):
    for task in tasks:
        ts = UsersTasks.objects.create(user=user_data.user, task=task)
        ts.rewards.add(*task.template.rewards.all())
        ts.save()


def place_jail(user_data:UserData, stage:Stage):
    amount = stage.stage_template.jail_amount
    tasks = random.sample(list(stage.get_empty_chests(user_data)), amount)
    for task in tasks:
        ts = UsersTasks.objects.create(user=user_data.user, task = task)
        ts.rewards.add(Reward.objects.get(name='Jail'))
        ts.save()


def place_items(user_data: UserData, rank:Rank):
    stages = rank.get_all_stages()
    for stage in stages:
        place_key(user_data, stage)
        place_jail(user_data, stage)
    place_rewards_for_chests(user_data, rank.get_empty_chests(user_data))
    place_another_tasks(user_data, rank.get_not_chest_tasks(user_data))
    ts = UsersTasks.objects.get(user=user_data.user, task=rank.init_stage.initial_task)
    ts.status = UsersTasks.Status.IN_PROGRESS
    ts.save()
