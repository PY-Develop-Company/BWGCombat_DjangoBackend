import os

from ads_app.models import Advert
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now
from exchanger_app.models import Asset, ExchangePair
from levels_app.models import Rank, TaskTemplate, TaskRoutes, Reward, MaxEnergyLevel, MulticlickLevel, \
    PassiveIncomeLevel, PartnerSocialTasks, CompletedPartnersTasks, StageTemplate, Stage
from user_app.models import User, Language, UserData, Link, Fren


class Command(BaseCommand):
    help = 'Seed database with initial data'

    tasks_1_stage = []

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.seed_energy_levels()
        self.seed_multiplier_levels()
        self.seed_passive_income_levels()

        self.seed_lang()

        self.seed_rewards()

        self.seed_task_templates()
        self.seed_task_routes()
        self.seed_links()

        self.seed_stage_templates()
        self.seed_stage()

        self.seed_ranks()

        self.seed_users()
        self.seed_frens()

        self.seed_social_media()
        # self.seed_completed_social_tasks()

        self.seed_superuser()

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

            {"id": 19, "name": "MULTICLICK_1", "amount": 1, "reward_type": Reward.RewardType.MULTIPLIER},
            {"id": 17, "name": "MULTICLICK_2", "amount": 2, "reward_type": Reward.RewardType.MULTIPLIER},
            {"id": 18, "name": "MULTICLICK_10", "amount": 10, "reward_type": Reward.RewardType.MULTIPLIER},
            # Add more rewards as needed
        ]
        for reward_data in rewards_data:
            Reward.objects.update_or_create(name=reward_data['name'], defaults=reward_data)

    def seed_ranks(self):
        ranks_data = [
            {"id": 4, "name": "Rank 4", "description": "Intermediate rank", "gold_required": 90000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_4")},
            {"id": 5, "name": "Rank 5", "description": "Intermediate rank", "gold_required": 120000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_5")},
            {"id": 6, "name": "Rank 6", "description": "Intermediate rank", "gold_required": 150000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_6")},
            {"id": 7, "name": "Rank 7", "description": "Intermediate rank", "gold_required": 180000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_7")},
            {"id": 8, "name": "Rank 8", "description": "Intermediate rank", "gold_required": 210000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_8")},
            {"id": 9, "name": "Rank 9", "description": "Intermediate rank", "gold_required": 240000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_9")},
            {"id": 10, "name": "Rank 10", "description": "Last rank", "gold_required": 300000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_10")},

            {"id": 3, "name": "Rank 3", "description": "Intermediate rank", "gold_required": 60000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_3"), 'init_stage_id': 5},
            {"id": 2, "name": "Вічна мерзлота", "description": "Intermediate rank", "gold_required": 30000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_2"), 'init_stage_id': 2,
             'next_rank_id': 3},
            {"id": 1, "name": "Ельфійський ліс", "description": "Starting rank", "gold_required": 10000,
             "inviter_reward": Reward.objects.get(name="Fren_Rank_1"), 'init_stage_id': 1,
             'next_rank_id': 2},
            # Add more ranks as needed
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
            st, _ = Stage.objects.update_or_create(id=stage_data['id'], defaults=
            {
                "name": stage_data['name'],
                "initial_task_id": stage_data['initial_task_id'],
                "stage_template_id": stage_data['stage_template_id'],
                "next_stage_id": stage_data.get('next_stage_id', None)
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
             "task_type": TaskTemplate.TaskType.ch_sub, "completion_number": 1, "price": 0,
             "rewards": [Reward.objects.get(id=16), Reward.objects.get(id=17)]},
            {"id": 2, "name": "Invite 1 friends", "text": "Invite a friend to join.",
             "task_type": TaskTemplate.TaskType.inv_fren, "completion_number": 1, "price": 0,
             "rewards": [Reward.objects.get(id=16), Reward.objects.get(id=18)]},

            {"id": 3, "name": "chest_1000", "text": f"{desc}", "task_type": TaskTemplate.TaskType.buy_chest,
             "completion_number": 1, "price": 1_000,
             "rewards": [Reward.objects.get(id=2), Reward.objects.get(id=14), Reward.objects.get(id=15)]},
            {"id": 7, "name": "chest_2000", "text": f"{desc}", "task_type": TaskTemplate.TaskType.buy_chest,
             "completion_number": 1, "price": 2_000,
             "rewards": [Reward.objects.get(id=2), Reward.objects.get(id=14), Reward.objects.get(id=15)]},
            {"id": 11, "name": "chest_3000", "text": f"{desc}", "task_type": TaskTemplate.TaskType.buy_chest,
             "completion_number": 1, "price": 3_000,
             "rewards": [Reward.objects.get(id=2), Reward.objects.get(id=14), Reward.objects.get(id=15)]},

            {"id": 4, "name": "Upgrade pickaxe +2", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.buy_multiclick, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=17)]},
            {"id": 5, "name": "Upgrade energy", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.buy_energy, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=16)]},
            {"id": 6, "name": "Upgrade pickaxe +1", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.buy_multiclick, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=19)]},
            {"id": 8, "name": "Upgrade energy", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.buy_energy, "completion_number": 0, "price": 5_000,
             "rewards": [Reward.objects.get(id=16)]},
            {"id": 9, "name": "Upgrade pickaxe +2", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.buy_multiclick, "completion_number": 0, "price": 5_000,
             "rewards": [Reward.objects.get(id=17)]},
            {"id": 10, "name": "Upgrade energy +100", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.buy_energy, "completion_number": 0, "price": 2_000,
             "rewards": [Reward.objects.get(id=20)]},

            {"id": 12, "name": "Upgrade energy +100", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.buy_energy, "completion_number": 0, "price": 10_000,
             "rewards": [Reward.objects.get(id=20)]},
            {"id": 13, "name": "Upgrade energy +50", "text": "Buy more energy",
             "task_type": TaskTemplate.TaskType.buy_energy, "completion_number": 0, "price": 10_000,
             "rewards": [Reward.objects.get(id=16)]},
            {"id": 14, "name": "Upgrade pickaxe +1", "text": "Earn more gold with 1 click",
             "task_type": TaskTemplate.TaskType.buy_multiclick, "completion_number": 0, "price": 5_000,
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
            task_route, created = TaskRoutes.objects.update_or_create(
                id=task_route_data['id'],
                defaults=task_route_data
            )
            task_route.save()

    def seed_energy_levels(self):
        energy_levels_data = [
            {"name": "Energy Level 1", "level": 1, "amount": 100},
            {"name": "Energy Level 2", "level": 2, "amount": 500},
            # Add more energy levels as needed
        ]
        for energy_level_data in energy_levels_data:
            MaxEnergyLevel.objects.update_or_create(name=energy_level_data['name'], defaults=energy_level_data)

    def seed_multiplier_levels(self):
        multiplier_levels_data = [
            {"name": "Multiplier Level 1", "level": 1, "amount": 1},
            {"name": "Multiplier Level 2", "level": 2, "amount": 4},
            # Add more multiplier levels as needed
        ]
        for multiplier_level_data in multiplier_levels_data:
            MulticlickLevel.objects.update_or_create(name=multiplier_level_data['name'], defaults=multiplier_level_data)

    def seed_passive_income_levels(self):
        passive_income_levels_data = [
            {"name": "Passive Income Level 1", "level": 1, "amount": 100},
            {"name": "Passive Income Level 2", "level": 2, "amount": 200},
            # Add more passive income levels as needed
        ]
        for passive_income_level_data in passive_income_levels_data:
            PassiveIncomeLevel.objects.update_or_create(name=passive_income_level_data['name'],
                                                        defaults=passive_income_level_data)

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
        user_data = [
            {'user': User.objects.get(tg_id=123568), 'character_gender': 0, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': Rank.objects.get(name="Ельфійський ліс"),
             'multiclick_amount': MulticlickLevel.objects.get(name="Multiplier Level 1").amount,
             'energy_regeneration': Rank.objects.get(name="Ельфійський ліс").init_energy_regeneration,
             'max_energy_amount': MaxEnergyLevel.objects.get(name="Energy Level 1").amount,
             'current_energy': MaxEnergyLevel.objects.get(name="Energy Level 1").amount,
             'passive_income_level': PassiveIncomeLevel.objects.get(name="Passive Income Level 1")},
            {'user': User.objects.get(tg_id=123456), 'character_gender': 1, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': Rank.objects.get(name="Ельфійський ліс"),
             'multiclick_amount': MulticlickLevel.objects.get(name="Multiplier Level 1").amount,
             'energy_regeneration': Rank.objects.get(name="Ельфійський ліс").init_energy_regeneration,
             'max_energy_amount': MaxEnergyLevel.objects.get(name="Energy Level 1").amount,
             'current_energy': MaxEnergyLevel.objects.get(name="Energy Level 1").amount,
             'passive_income_level': PassiveIncomeLevel.objects.get(name="Passive Income Level 1")},
            {'user': User.objects.get(tg_id=123457), 'character_gender': None, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': Rank.objects.get(name="Ельфійський ліс"),
             'multiclick_amount': MulticlickLevel.objects.get(name="Multiplier Level 1").amount,
             'energy_regeneration': Rank.objects.get(name="Ельфійський ліс").init_energy_regeneration,
             'max_energy_amount': MaxEnergyLevel.objects.get(name="Energy Level 1").amount,
             'current_energy': MaxEnergyLevel.objects.get(name="Energy Level 1").amount,
             'passive_income_level': PassiveIncomeLevel.objects.get(name="Passive Income Level 1")},
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

    def seed_social_media(self):
        social_medias = [
            {"id": 1, "name_en": "Facebook", "link": "https://www.facebook.com", "reward_amount": 5000,
             "is_partner": True},
            {"id": 2, "name_en": "Twitter", "link": "https://www.twitter.com", "reward_amount": 3000, "is_partner": False},
            {"id": 3, "name_en": "Instagram", "link": "https://www.instagram.com", "reward_amount": 4000,
             "is_partner": True}
        ]
        for data in social_medias:
            PartnerSocialTasks.objects.update_or_create(id=data['id'], defaults=data)

    def seed_completed_social_tasks(self):
        tasks = [
            {"user": User.objects.get(tg_id=123456), "task": PartnerSocialTasks.objects.get(id=1)},
            {"user": User.objects.get(tg_id=123456), "task": PartnerSocialTasks.objects.get(id=2)},
            {"user": User.objects.get(tg_id=123568), "task": PartnerSocialTasks.objects.get(id=2)},
        ]
        for data in tasks:
            CompletedPartnersTasks.objects.update_or_create(data)

    def seed_ads(self):
        ads = [
            {"id": 1, "name": "Azino 777", "description": "Vygravaytie 100000000000000000000 rubley",
             "link": Link.objects.get(id=1), "image_path": "azino777.jfif"}
        ]
        for data in ads:
            Advert.objects.update_or_create(id=data['id'], defaults=data)
