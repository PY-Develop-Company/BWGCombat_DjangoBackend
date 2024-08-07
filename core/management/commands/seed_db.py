import os

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from ads_app.models import BannerAdvert, FullscreenAdvert
from exchanger_app.models import Asset, ExchangePair
from levels_app.models import (Rank, TaskTemplate, TaskRoute, Reward, \
                               PartnersTasks, SocialTasks, CompletedSocialTasks, CompletedPartnersTasks, StageTemplate, \
                               Stage, PartnersButtonTypes)
from clicker_app.models import EnergyBalanceUpgradeLevel, MulticlickUpgradeLevel
from user_app.models import User, Language, UserData, Link, Fren


class Command(BaseCommand):
    help = 'Seed database with initial data'

    tasks_1_stage = []

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.seed_energy_balance_levels()
        self.seed_multiclick_levels()

        self.seed_lang()

        self.seed_rewards()

        self.seed_task_templates()
        self.seed_task_routes()
        self.seed_links()

        self.seed_stage_templates()
        self.seed_stage()

        self.seed_ranks()

        self.seed_users()
        self.seed_superuser()
        self.seed_user_data()

        self.seed_frens()

        self.seed_partners_task_buttons()
        self.seed_social_tasks()
        self.seed_partners_tasks()
        self.seed_completed_partners_tasks()
        self.seed_completed_social_tasks()

        self.seed_assets()
        self.seed_exchange_pairs()
        self.seed_ads()

        self.stdout.write('Data seeded successfully.')

    def seed_lang(self):
        lang_data = [
            {'lang_code': 'en', 'lang_name': 'English'},
            {'lang_code': 'uk', 'lang_name': 'Ukrainian'},
        ]
        for data in lang_data:
            Language.objects.update_or_create(lang_code=data['lang_code'], defaults=data)

    def seed_rewards(self):
        rewards_data = [
            {"id": 1, "name": "KEY_1", "amount": 1, "reward_type": Reward.RewardType.KEY},
            {"id": 2, "name": "GNOME_1", "amount": 1, "reward_type": Reward.RewardType.GNOME},
            {"id": 3, "name": "JAIL_12", "amount": 12, "reward_type": Reward.RewardType.JAIL},

            {"id": 4, "name": "Fren_Rank_1", "amount": 0.0009765625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 5, "name": "Fren_Rank_2", "amount": 0.001953125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 6, "name": "Fren_Rank_3", "amount": 0.00390625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 7, "name": "Fren_Rank_4", "amount": 0.0078125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 8, "name": "Fren_Rank_5", "amount": 0.015625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 9, "name": "Fren_Rank_6", "amount": 0.03125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 10, "name": "Fren_Rank_7", "amount": 0.0625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 11, "name": "Fren_Rank_8", "amount": 0.125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 12, "name": "Fren_Rank_9", "amount": 0.25, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 13, "name": "Fren_Rank_10", "amount": 0.5, "reward_type": Reward.RewardType.G_TOKEN},

            {"id": 14, "name": "GOLD_POSITIVE_1000", "amount": 1000, "reward_type": Reward.RewardType.GOLD},
            {"id": 15, "name": "GOLD_NEGATIVE_1000", "amount": -1000, "reward_type": Reward.RewardType.GOLD},

            {"id": 16, "name": "ENERGY_50", "amount": 50, "reward_type": Reward.RewardType.ENERGY_BALANCE},
            {"id": 20, "name": "ENERGY_100", "amount": 100, "reward_type": Reward.RewardType.ENERGY_BALANCE},

            {"id": 19, "name": "MULTICLICK_1", "amount": 1, "reward_type": Reward.RewardType.MULTICKLICK},
            {"id": 17, "name": "MULTICLICK_2", "amount": 2, "reward_type": Reward.RewardType.MULTICKLICK},
            {"id": 18, "name": "MULTICLICK_10", "amount": 10, "reward_type": Reward.RewardType.MULTICKLICK},

            {"id": 21, "name": "Ad_View_MAX_GOLD", "amount": 2000, "reward_type": Reward.RewardType.GOLD},
            {"id": 22, "name": "Ad_View_MIN_GOLD", "amount": 500, "reward_type": Reward.RewardType.GOLD},
            # Add more rewards as needed
        ]
        for reward_data in rewards_data:
            Reward.objects.update_or_create(name=reward_data['name'], defaults=reward_data)

    def seed_ranks(self):
        ranks_data = [
            {"id": 10, "init_energy_balance": 100, "init_multiclick": 8,
             "name": "Rank 10", "description": "Last rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_10"),
             "gold_required": 1000000},
            {"id": 9, "init_energy_balance": 300, "init_multiclick": 10,
             "name": "Rank 9", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_9"),
             "gold_required": 900000,
             'next_rank_id': 10},
            {"id": 8, "init_energy_balance": 300, "init_multiclick": 10,
             "name": "Rank 8", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_8"),
             "gold_required": 800000,
             'next_rank_id': 9},
            {"id": 7, "init_energy_balance": 200, "init_multiclick": 8,
             "name": "Rank 7", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_7"),
             "gold_required": 700000,
             'next_rank_id': 8},
            {"id": 6, "init_energy_balance": 100, "init_multiclick": 8,
             "name": "Rank 6", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_6"),
             "gold_required": 500000,
             'next_rank_id': 7},
            {"id": 5, "init_energy_balance": 100, "init_multiclick": 6,
             "name": "Rank 5", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_5"),
             "gold_required": 300000,
             'next_rank_id': 6},
            {"id": 4, "init_energy_balance": 100, "init_multiclick": 4,
             "name": "Rank 4", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_4"),
             "gold_required": 100000,
             'next_rank_id': 5},
            {"id": 3, "init_energy_balance": 100, "init_multiclick": 2,
             "name": "Rank 3", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_3"),
             "gold_required": 50000,
             'init_stage_id': 5}, #, 'next_rank_id': 4},
            {"id": 2, "init_energy_balance": 100, "init_multiclick": 2,
             "name": "2 Вічна мерзлота", "description": "Intermediate rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_2"),
             "gold_required": 20000,
             'init_stage_id': 2, 'next_rank_id': 3},
            {"id": 1, "init_energy_balance": 100, "init_multiclick": 2,
             "name": "1 Ельфійський ліс", "description": "Starting rank",
             "inviter_reward": Reward.objects.get(name="Fren_Rank_1"),
             "gold_required": 10000,
             'init_stage_id': 1, 'next_rank_id': 2},
        ]
        for rank_data in ranks_data:
            next_rank = rank_data.pop('next_rank_id', None)
            rank, _ = Rank.objects.update_or_create(name=rank_data['name'], defaults=rank_data)
            rank.next_rank_id = next_rank
            rank.save()

    def seed_stage_templates(self):
        stage_temp_data = [
            {"id": 1, "name": "1_stage_1_rank", "keys_amount": 0, "jail_amount": 0, 'task_with_keys': []},
            {"id": 2, "name": "1_stage_2_rank", "keys_amount": 0, "jail_amount": 0, 'task_with_keys': []},
            {"id": 3, "name": "1_stage_3_rank", "keys_amount": 1, "jail_amount": 2,
             'task_with_keys': {16, 17, 20, 24, 26, 27, 29}},

            {"id": 4, "name": "2_stage_3_rank", "keys_amount": 1, "jail_amount": 2,
             'task_with_keys': {34, 35, 39, 47, 48, 44, 45}},
            {"id": 5, "name": "3_stage_3_rank", "keys_amount": 1, "jail_amount": 2,
             'task_with_keys': {62, 63, 65, 67, 56, 58, 53, 54}},
        ]
        for stage_temp in stage_temp_data:
            st, _ = StageTemplate.objects.update_or_create(
                id=stage_temp['id'], defaults={
                    "name": stage_temp['name'],
                    'keys_amount': stage_temp['keys_amount'],
                    "jail_amount": stage_temp['jail_amount']})
            for i in stage_temp['task_with_keys']:
                st.task_with_keys.add(i)
            st.save()

    def seed_stage(self):
        rank_2_stage_1_tasks_ids = list(range(3, 11))
        rank_3_stage_1_tasks_ids = list(range(11, 30))
        rank_3_stage_2_tasks_ids = list(range(30, 49))
        rank_3_stage_3_tasks_ids = list(range(49, 68))
        stage_data = [
            {"id": 1, "name": "1_stage_1_rank", "initial_task_id": 1, "tasks": [1, 2],
             "stage_template_id": 1, "has_keylock": False},
            {"id": 2, "name": "1_stage_2_rank", "initial_task_id": 3, "tasks": rank_2_stage_1_tasks_ids,
             "stage_template_id": 2, "has_keylock": False},
            {"id": 3, "name": "3_stage_3_rank", "initial_task_id": 49, "tasks": rank_3_stage_3_tasks_ids,
             "stage_template_id": 5},
            {"id": 4, "name": "2_stage_3_rank", "initial_task_id": 30, "tasks": rank_3_stage_2_tasks_ids,
             "stage_template_id": 4, 'next_stage_id': 3},
            {"id": 5, "name": "1_stage_3_rank", "initial_task_id": 11, "tasks": rank_3_stage_1_tasks_ids,
             "stage_template_id": 3, 'next_stage_id': 4},
        ]

        for stage_data in stage_data:
            upgrade_id = stage_data.get("id") - 1
            instrument = MulticlickUpgradeLevel.objects.get(level=upgrade_id)
            drink = EnergyBalanceUpgradeLevel.objects.get(level=upgrade_id)
            st, _ = Stage.objects.update_or_create(id=stage_data['id'], defaults=
            {
                "name": stage_data['name'],
                "initial_task_id": stage_data['initial_task_id'],
                "stage_template_id": stage_data['stage_template_id'],
                "next_stage_id": stage_data.get('next_stage_id', None),
                "instrument": instrument,
                "drink": drink,
            })
            if "has_keylock" in stage_data.keys():
                st.has_keylock = stage_data['has_keylock']
            st.tasks.add(*stage_data['tasks'])
            st.save()

    @transaction.atomic
    def seed_task_templates(self):
        desc = "Buy chest and get chance to get extra gnome"
        task_templates_data = [
            {"id": 1, "name": "Subscribe to Channel", "text": "Subscribe to our channel.",
             "task_type": TaskTemplate.TaskType.SUBSCRIPTION, "completion_number": 1, "price": 0,
             "rewards": [Reward.objects.get(id=16), Reward.objects.get(id=17)]},
            {"id": 2, "name": "Invite 1 friends", "text": "Invite a friend to join.",
             "task_type": TaskTemplate.TaskType.INVITE_FREN, "completion_number": 1, "price": 0,
             "rewards": [Reward.objects.get(id=16), Reward.objects.get(id=18)]},

            {"id": 3, "name": "chest_1000", "text": f"{desc}", "task_type": TaskTemplate.TaskType.BUY_CHEST,
             "completion_number": 1, "price": 1_000,
             "rewards": [Reward.objects.get(id=2), Reward.objects.get(id=14), Reward.objects.get(id=15)]},
            {"id": 7, "name": "chest_2000", "text": f"{desc}", "task_type": TaskTemplate.TaskType.BUY_CHEST,
             "completion_number": 1, "price": 2_000,
             "rewards": [Reward.objects.get(id=2), Reward.objects.get(id=14), Reward.objects.get(id=15)]},
            {"id": 11, "name": "chest_3000", "text": f"{desc}", "task_type": TaskTemplate.TaskType.BUY_CHEST,
             "completion_number": 1, "price": 3_000,
             "rewards": [Reward.objects.get(id=2), Reward.objects.get(id=14), Reward.objects.get(id=15)]},

            {"id": 4, "name": "Upgrade pickaxe +2", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.BUY_MULTICLICK, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=17)]},
            {"id": 5, "name": "Upgrade energy", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.BUY_ENERGY_BALANCE, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=16)]},
            {"id": 6, "name": "Upgrade pickaxe +1", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.BUY_MULTICLICK, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=19)]},
            {"id": 8, "name": "Upgrade energy", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.BUY_ENERGY_BALANCE, "completion_number": 0, "price": 5_000,
             "rewards": [Reward.objects.get(id=16)]},
            {"id": 9, "name": "Upgrade pickaxe +2", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.BUY_MULTICLICK, "completion_number": 0, "price": 5_000,
             "rewards": [Reward.objects.get(id=17)]},
            {"id": 10, "name": "Upgrade energy +100", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.BUY_ENERGY_BALANCE, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=20)]},

            {"id": 12, "name": "Upgrade energy +100", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.BUY_ENERGY_BALANCE, "completion_number": 0, "price": 10_000,
             "rewards": [Reward.objects.get(id=20)]},
            {"id": 13, "name": "Upgrade energy +50", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.BUY_ENERGY_BALANCE, "completion_number": 0, "price": 10_000,
             "rewards": [Reward.objects.get(id=16)]},
            {"id": 14, "name": "Upgrade pickaxe +1", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.BUY_MULTICLICK, "completion_number": 0, "price": 5_000,
             "rewards": [Reward.objects.get(id=19)]},

            # Add more task templates as needed
        ]

        for task_template_data in task_templates_data:
            rewards = task_template_data.pop("rewards", [])
            task_template, created = TaskTemplate.objects.update_or_create(
                id=task_template_data['id'],
                defaults=task_template_data
            )
            task_template.rewards.set(rewards)
            task_template.save()

    @transaction.atomic
    def seed_task_routes(self):
        task_routes_data = [
            {"id": 1, "coord_x": 0, "coord_y": 0, "template_id": 1, "parent": None, "initial": True},
            {"id": 2, "coord_x": 0, "coord_y": -1, "template_id": 2, "parent_id": 1, "initial": False},
            # 2 rank 1 stage
          
            {"id": 3, "coord_x": 0, "coord_y": 0, "template_id": 5, "parent_id": None, "initial": True},
            {"id": 4, "coord_x": -1, "coord_y": 0, "template_id": 4, "parent_id": 3, "initial": False},
            {"id": 5, "coord_x": -2, "coord_y": 0, "template_id": 3, "parent_id": 4, "initial": False},
            {"id": 6, "coord_x": 1, "coord_y": 0, "template_id": 3, "parent_id": 3, "initial": False},
            {"id": 7, "coord_x": 0, "coord_y": -1, "template_id": 8, "parent_id": 3, "initial": False},
            {"id": 8, "coord_x": -1, "coord_y": -1, "template_id": 9, "parent_id": 7, "initial": False},
            {"id": 9, "coord_x": 0, "coord_y": -2, "template_id": 8, "parent_id": 7, "initial": False},
            {"id": 10, "coord_x": -1, "coord_y": -2, "template_id": 9, "parent_id": 9, "initial": False},
          
            # 3 rank 1 stage(left)
            {"id": 11, "coord_x": 0, "coord_y": 0, "template_id": 5, "parent_id": None, "initial": True},
            {"id": 12, "coord_x": -1, "coord_y": 0, "template_id": 6, "parent_id": 11, "initial": False},
            {"id": 13, "coord_x": -2, "coord_y": 0, "template_id": 3, "parent_id": 12, "initial": False},
          
            # central
            {"id": 14, "coord_x": -3, "coord_y": 0, "template_id": 3, "parent_id": 13, "initial": False},
            {"id": 15, "coord_x": -2, "coord_y": -1, "template_id": 3, "parent_id": 13, "initial": False},
            {"id": 16, "coord_x": -3, "coord_y": -1, "template_id": 3, "parent_id": 15, "initial": False},  # key
            {"id": 17, "coord_x": -1, "coord_y": -1, "template_id": 3, "parent_id": 15, "initial": False},  # key
            {"id": 18, "coord_x": -2, "coord_y": 1, "template_id": 3, "parent_id": 13, "initial": False},
            {"id": 19, "coord_x": -3, "coord_y": 1, "template_id": 6, "parent_id": 18, "initial": False},
            {"id": 20, "coord_x": -1, "coord_y": 1, "template_id": 3, "parent_id": 18, "initial": False},  # key
          
            # 3 rank 1 stage(right)
            {"id": 21, "coord_x": 1, "coord_y": 0, "template_id": 3, "parent_id": 11, "initial": True},
            {"id": 22, "coord_x": 2, "coord_y": 0, "template_id": 3, "parent_id": 21, "initial": False},
            {"id": 23, "coord_x": 2, "coord_y": -1, "template_id": 3, "parent_id": 22, "initial": False},
            {"id": 24, "coord_x": 1, "coord_y": -1, "template_id": 3, "parent_id": 23, "initial": False},  # key
            {"id": 25, "coord_x": 3, "coord_y": 0, "template_id": 5, "parent_id": 22, "initial": False},
            {"id": 26, "coord_x": 3, "coord_y": -1, "template_id": 3, "parent_id": 25, "initial": False},  # key
            {"id": 27, "coord_x": 3, "coord_y": 1, "template_id": 3, "parent_id": 25, "initial": False},  # key
            {"id": 28, "coord_x": 2, "coord_y": 1, "template_id": 3, "parent_id": 27, "initial": False},
            {"id": 29, "coord_x": 1, "coord_y": 1, "template_id": 3, "parent_id": 28, "initial": False},  # key
          
            # 3 rank 2 stage
            {"id": 30, "coord_x": 0, "coord_y": 0, "template_id": 8, "parent_id": None, "initial": True},
            {"id": 31, "coord_x": 1, "coord_y": 0, "template_id": 8, "parent_id": 30, "initial": False},
            {"id": 32, "coord_x": 2, "coord_y": 0, "template_id": 7, "parent_id": 31, "initial": False},
            {"id": 33, "coord_x": 2, "coord_y": 1, "template_id": 7, "parent_id": 32, "initial": False},
            {"id": 34, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 33, "initial": False},  # key
            {"id": 35, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 33, "initial": False},  # key
            {"id": 36, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 35, "initial": False},
            {"id": 37, "coord_x": 1, "coord_y": 1, "template_id": 10, "parent_id": 36, "initial": False},
            {"id": 38, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 37, "initial": False},
            {"id": 39, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 38, "initial": False},  # key
            {"id": 40, "coord_x": 1, "coord_y": 1, "template_id": 9, "parent_id": 30, "initial": False},
            {"id": 41, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 40, "initial": False},
            {"id": 42, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 41, "initial": False},
            {"id": 43, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 41, "initial": False},
            {"id": 44, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 42, "initial": False},  # key
            {"id": 45, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 42, "initial": False},  # key
            {"id": 46, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 41, "initial": False},
            {"id": 47, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 46, "initial": False},  # key
            {"id": 48, "coord_x": 1, "coord_y": 1, "template_id": 7, "parent_id": 46, "initial": False},  # key
          
            # 3 rank 3 stage
            {"id": 49, "coord_x": 0, "coord_y": 0, "template_id": 12, "parent_id": None, "initial": True},
            {"id": 50, "coord_x": 1, "coord_y": 0, "template_id": 11, "parent_id": 49, "initial": False},
            {"id": 51, "coord_x": 2, "coord_y": 0, "template_id": 11, "parent_id": 50, "initial": False},
            {"id": 52, "coord_x": 2, "coord_y": -1, "template_id": 11, "parent_id": 51, "initial": False},
            {"id": 53, "coord_x": 1, "coord_y": -1, "template_id": 11, "parent_id": 52, "initial": False},  # key
            {"id": 54, "coord_x": 3, "coord_y": -1, "template_id": 11, "parent_id": 52, "initial": False},  # key
            {"id": 55, "coord_x": 3, "coord_y": 0, "template_id": 13, "parent_id": 54, "initial": False},
            {"id": 56, "coord_x": 3, "coord_y": 1, "template_id": 11, "parent_id": 55, "initial": False},  # key
            {"id": 57, "coord_x": 2, "coord_y": 1, "template_id": 11, "parent_id": 51, "initial": False},
            {"id": 58, "coord_x": 1, "coord_y": 1, "template_id": 11, "parent_id": 57, "initial": False},  # key
            {"id": 59, "coord_x": -1, "coord_y": 0, "template_id": 14, "parent_id": 49, "initial": False},
            {"id": 60, "coord_x": -2, "coord_y": 0, "template_id": 11, "parent_id": 59, "initial": False},
            {"id": 61, "coord_x": -2, "coord_y": 1, "template_id": 11, "parent_id": 60, "initial": False},
            {"id": 62, "coord_x": -1, "coord_y": 1, "template_id": 11, "parent_id": 61, "initial": False},  # key
            {"id": 63, "coord_x": -3, "coord_y": 1, "template_id": 11, "parent_id": 61, "initial": False},  # key
            {"id": 64, "coord_x": -3, "coord_y": 0, "template_id": 14, "parent_id": 63, "initial": False},
            {"id": 65, "coord_x": -3, "coord_y": -1, "template_id": 11, "parent_id": 64, "initial": False},  # key
            {"id": 66, "coord_x": -2, "coord_y": -1, "template_id": 11, "parent_id": 65, "initial": False},
            {"id": 67, "coord_x": -1, "coord_y": -1, "template_id": 11, "parent_id": 66, "initial": False},  # key
        ]

        for task_route_data in task_routes_data:
            task_route, created = TaskRoute.objects.update_or_create(
                id=task_route_data['id'],
                defaults=task_route_data
            )
            task_route.save()

    def seed_energy_balance_levels(self):
        energy_levels_data = [
            {"level": 0, "name": "Заряд Адреналіну"},
            {"level": 1, "name": "Енергетичний Коктейль"},
            {"level": 2, "name": "Еліксир Сили"},
            {"level": 3, "name": "Потужний Напій"},
            {"level": 4, "name": "Тонік Мудрості"},
            {"level": 5, "name": "Енергетичний Бустер"},
            {"level": 6, "name": "Напій Свіжості"},
            {"level": 7, "name": "Вітамінний Коктейль"},
            {"level": 8, "name": "Сила Титана"},
            {"level": 9, "name": "Вітамінний Напій"},
            {"level": 10, "name": "Еліксир Життя"},
            {"level": 11, "name": "Магічний Тонік"},
            {"level": 12, "name": "Напій Сили"},
            {"level": 13, "name": "Тонік Витривалості"},
            {"level": 14, "name": "Заряд Бадьорості"},
            {"level": 15, "name": "Еліксир Енергії"},
            {"level": 16, "name": "Потужний Бустер"},
            {"level": 17, "name": "Напій Мудрості"},
            {"level": 18, "name": "Енергетичний Еліксир"},
            {"level": 19, "name": "Сила Дракона"},
            {"level": 20, "name": "Тонік Здоров'я"},
            {"level": 21, "name": "Заряд Витривалості"},
            {"level": 22, "name": "Еліксир Свіжості"},
            {"level": 23, "name": "Напій Лева"},
            {"level": 24, "name": "Вітамінний Бустер"},
            {"level": 25, "name": "Енергетичний Тонік"},
            {"level": 26, "name": "Потужний Еліксир"},
            {"level": 27, "name": "Напій Сили2"},
            {"level": 28, "name": "Тонік Бадьорості"},
            {"level": 29, "name": "Еліксир Мудрості"},
            {"level": 30, "name": "Заряд Енергії"},
            {"level": 31, "name": "Вітамінний Еліксир"},
            {"level": 32, "name": "Енергетичний Напій"},
            {"level": 33, "name": "Сила Вовка"},
            {"level": 34, "name": "Тонік Свіжості"},
            {"level": 35, "name": "Еліксир Витривалості"},
            {"level": 36, "name": "Потужний Напій2"},
            {"level": 37, "name": "Напій Здоров'я"},
            {"level": 38, "name": "Енергетичний Заряд"},
            {"level": 39, "name": "Заряд Сили"},
            {"level": 40, "name": "Тонік Сили"},
            {"level": 41, "name": "Еліксир Бадьорості"},
            {"level": 42, "name": "Напій Енергії"},
            {"level": 43, "name": "Сила Мудрості"},
            {"level": 44, "name": "Вітамінний Заряд"},
            {"level": 45, "name": "Потужний Тонік"}
        ]
        for energy_level_data in energy_levels_data:
            EnergyBalanceUpgradeLevel.objects.update_or_create(name=energy_level_data['name'], defaults=energy_level_data)

    def seed_multiclick_levels(self):
        multiclick_levels_data = [
            {"level": 0, "name": "Залізний Дробар"},
            {"level": 1, "name": "Полум'яний Молот"},
            {"level": 2, "name": "Червоний Тесак"},
            {"level": 3, "name": "Вогняний Дробар"},
            {"level": 4, "name": "Демонічний Клівер"},
            {"level": 5, "name": "Золотий Сокирка"},
            {"level": 6, "name": "Льодовий Різець"},
            {"level": 7, "name": "Плазмовий Гармаш"},
            {"level": 8, "name": "Електричний Дробар"},
            {"level": 9, "name": "Холодний Молот"},
            {"level": 10, "name": "Палаючий Двійник"},
            {"level": 11, "name": "Дерев'яний Обух"},
            {"level": 12, "name": "Енергетичний Топір"},
            {"level": 13, "name": "Містичний Тесак"},
            {"level": 14, "name": "Титанічний Топір"},
            {"level": 15, "name": "Кам'яний Молот"},
            {"level": 16, "name": "Кришталева Лопата"},
            {"level": 17, "name": "Крижаний Топір"},
            {"level": 18, "name": "Блискавичний Різець"},
            {"level": 19, "name": "Ржавий Тесак"},
            {"level": 20, "name": "Зоряний Тесак"},
            {"level": 21, "name": "Бойова Лопата"},
            {"level": 22, "name": "Кібернетичний Молот"},
            {"level": 23, "name": "Плетений Обух"},
            {"level": 24, "name": "Магічний Сокирка"},
            {"level": 25, "name": "Стародавній Топір"},
            {"level": 26, "name": "Сяючий Дробар"},
            {"level": 27, "name": "Футуристичний Різець"},
            {"level": 28, "name": "Механічний Молот"},
            {"level": 29, "name": "Космічний Топір"},
            {"level": 30, "name": "Глиняний Тесак"},
            {"level": 31, "name": "Драконячий Дробар"},
            {"level": 32, "name": "Обсидіановий Топір"},
            {"level": 33, "name": "Бойовий Молот"},
            {"level": 34, "name": "Квантовий Тесак"},
            {"level": 35, "name": "Золотий Клівер"},
            {"level": 36, "name": "Теслярський Обух"},
            {"level": 37, "name": "Палаючий Тесак"},
            {"level": 38, "name": "Льодовий Двійник"},
            {"level": 39, "name": "Крижаний Коготь"},
            {"level": 40, "name": "Сяючий Тесак"},
            {"level": 41, "name": "Містичний Молот"},
            {"level": 42, "name": "Крилатий Тесак"},
            {"level": 43, "name": "Льодовий Клівер"},
            {"level": 44, "name": "Вогняний Коготь"},
            {"level": 45, "name": "Драконячий Коготь"}
        ]
        for multiclick_level_data in multiclick_levels_data:
            MulticlickUpgradeLevel.objects.update_or_create(name=multiclick_level_data['name'], defaults=multiclick_level_data)

    def seed_links(self):
        links = [
            {"url": os.environ.get("TG_CHANNEL"), "task": TaskTemplate.objects.get(name="Subscribe to Channel")}
        ]
        for data in links:
            Link.objects.update_or_create(url=data['url'], defaults=data)

    def seed_users(self):
        users = [
            {'tg_id': 123568, 'tg_username': 'test_mister', 'firstname': 'mister', 'lastname': 'test',
             'interface_lang': Language.objects.get(lang_code='en'), 'last_login': now()},
            {'tg_id': 123456, 'tg_username': 'test_miss', 'firstname': 'miss', 'lastname': 'test',
             'interface_lang': Language.objects.get(lang_code='en'), 'last_login': now()},
            {'tg_id': 123457, 'tg_username': 'test_none', 'firstname': 'miss', 'lastname': 'test',
             'interface_lang': Language.objects.get(lang_code='en'), 'last_login': now()},
        ]
        for data in users:
            User.objects.update_or_create(tg_id=data['tg_id'], defaults=data)

    def seed_frens(self):
        frens = [
            {'fren_tg': User.objects.get(tg_id=123456), 'inviter_tg': User.objects.get(tg_id=123568)},
            {'fren_tg': User.objects.get(tg_id=123456), 'inviter_tg': User.objects.get(tg_id=123568)}
        ]
        for data in frens:
            Fren.objects.update_or_create(defaults=data)

    def seed_user_data(self):
        first_rank = Rank.objects.get(id=1)
        user_data = [
            {'user': User.objects.get(tg_id=os.environ.get("ADMIN_TG_ID")), 'character_gender': 0, 'gold_balance': 2_000_000, 'g_token': 20,
             'last_visited': now(), 'rank': first_rank,
             'energy_regeneration': first_rank.init_energy_regeneration,
             'gnome_amount': 3},
            {'user': User.objects.get(tg_id=123568), 'character_gender': 0, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': first_rank,
             'energy_regeneration': first_rank.init_energy_regeneration,
             'gnome_amount': 0},
            {'user': User.objects.get(tg_id=123456), 'character_gender': 1, 'gold_balance': 1_500_000, 'g_token': 35,
             'last_visited': now(), 'rank': first_rank,
             'energy_regeneration': first_rank.init_energy_regeneration,
             'gnome_amount': 4},
            {'user': User.objects.get(tg_id=123457), 'character_gender': None, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': first_rank,
             'energy_regeneration': first_rank.init_energy_regeneration,
             'gnome_amount': 0}
        ]
        for data in user_data:
            UserData.objects.update_or_create(user=data['user'], defaults=data)

    def seed_superuser(self):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(tg_id=os.environ.get("ADMIN_TG_ID"),
                                          tg_username=os.environ.get("ADMIN_USERNAME"), firstname='admin',
                                          lastname='admin', password=os.environ.get("ADMIN_PASSWORD"))

    def seed_assets(self):
        assets = [
            {"id": 1, "name": "G-Token"},
            {"id": 2, "name": "Gold"},
            {"id": 3, "name": "Gnome"}
        ]
        for data in assets:
            Asset.objects.update_or_create(id=data['id'], defaults=data)

    def seed_exchange_pairs(self):
        pairs = [
            {"id": 1, "asset_1": Asset.objects.get(id=1), "asset_2": Asset.objects.get(id=2),
             "rate": 100_000},
            {"id": 2, "asset_1": Asset.objects.get(id=2), "asset_2": Asset.objects.get(id=1),
             "rate": 0.00001},
            {"id": 3, "asset_1": Asset.objects.get(id=1), "asset_2": Asset.objects.get(id=3),
             "rate": 0.333333333333, "fee_percentage": None},
            {"id": 4, "asset_1": Asset.objects.get(id=3), "asset_2": Asset.objects.get(id=1),
             "rate": 6, "fee_percentage": None}
        ]
        for data in pairs:
            ExchangePair.objects.update_or_create(id=data['id'], defaults=data)

    def seed_partners_task_buttons(self):
        social_medias = [
            {"id": 1, "name_en": "Play", "name_de": "Spielen", "name_fr": "Jouer", "name_ru": "Играть",
             "name_uk": "Грати", "name_zh": "游戏"},
            {"id": 2, "name_en": "Register", "name_de": "Register", "name_fr": "Registre", "name_ru": "Регистрация",
             "name_uk": "Зареєструйся", "name_zh": "注册"},
            {"id": 2, "name_en": "Subscribe", "name_de": "Abonnieren", "name_fr": "S'abonner", "name_ru": "Подписаться",
             "name_uk": "Підписатись", "name_zh": "订阅"},
        ]
        for data in social_medias:
            PartnersButtonTypes.objects.update_or_create(id=data['id'], defaults=data)

    def seed_social_tasks(self):
        social_tasks = [
            {"id": 1, "link": "https://www.facebook.com", "reward_amount": 5000,
             "name_en": "Facebook english", "name_de": "Facebook deutsch", "name_fr": "Facebook franc",
             "name_ru": "Facebook ru", "name_uk": "Facebook uk", "name_zh": "Facebook zh"},
            {"id": 2, "link": "https://www.twitter.com", "reward_amount": 3000,
             "name_en": "Facebook english", "name_de": "Facebook deutsch", "name_fr": "Facebook franc",
             "name_ru": "Facebook ru", "name_uk": "Facebook uk", "name_zh": "Facebook zh"},
            {"id": 3, "link": "https://www.instagram.com", "reward_amount": 4000,
             "name_en": "Facebook english", "name_de": "Facebook deutsch", "name_fr": "Facebook franc",
             "name_ru": "Facebook ru", "name_uk": "Facebook uk", "name_zh": "Facebook zh"}
        ]
        for data in social_tasks:
            SocialTasks.objects.update_or_create(id=data['id'], defaults=data)

    def seed_completed_social_tasks(self):
        tasks = [
            {"user": User.objects.get(tg_id=123568), "task": SocialTasks.objects.get(id=1)},
            {"user": User.objects.get(tg_id=123456), "task": SocialTasks.objects.get(id=2)},
        ]
        for data in tasks:
            CompletedSocialTasks.objects.update_or_create(data)

    def seed_partners_tasks(self):
        partners_tasks = [
            {"id": 1, "name": "BWG", "button_type": PartnersButtonTypes.objects.get(id=2), "link": "https://t.me/BWGOLDEN_Bot", "reward_amount": 5000},
            {"id": 2, "name": "Catizen", "button_type": PartnersButtonTypes.objects.get(id=1), "link": "https://t.me/catizenbot", "reward_amount": 3000},
        ]
        for data in partners_tasks:
            PartnersTasks.objects.update_or_create(id=data['id'], defaults=data)

    def seed_completed_partners_tasks(self):
        tasks = [
            {"user": User.objects.get(tg_id=123568), "task": PartnersTasks.objects.get(id=1)},
            {"user": User.objects.get(tg_id=123456), "task": PartnersTasks.objects.get(id=2)},
        ]
        for data in tasks:
            CompletedPartnersTasks.objects.update_or_create(data)

    def seed_ads(self):
        banner_ads = [
            {"id": 1, "name": "Azino 777", "description": "Vygravaytie 100000000000000000000 rubley",
             "link": Link.objects.get(id=1), "file_path": "azino777.jfif"}
        ]
        fullscreen_ads = [
            {"id": 1, "name": "Azino 777", "description": "Vygravaytie 100000000000000000000 rubley",
             "link": Link.objects.get(id=1), "file_path": "azino777.jfif",
             "view_max_gold_reward": Reward.objects.get(name="Ad_View_MAX_GOLD"),
             "view_min_gold_reward": Reward.objects.get(name="Ad_View_MIN_GOLD"),
             "view_gnome_reward": Reward.objects.get(name="GNOME_1")}
        ]
        for data in banner_ads:
            BannerAdvert.objects.update_or_create(id=data['id'], defaults=data)
        for data in fullscreen_ads:
            FullscreenAdvert.objects.update_or_create(id=data['id'], defaults=data)
