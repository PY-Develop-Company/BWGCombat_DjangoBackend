from django.core.management.base import BaseCommand
from django.utils.timezone import now
from levels_app.models import Rank, Task, Reward, EnergyLevel, MultiplierLevel, PassiveIncomeLevel
from user_app.models import User, Language, UserData, CustomUserManager, Link
import os


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.seed_lang()
        self.seed_rewards()
        self.seed_ranks()
        self.seed_tasks()
        self.seed_energy_levels()
        self.seed_multiplier_levels()
        self.seed_passive_income_levels()
        self.seed_links()
        self.seed_users()
        self.seed_user_data()
        self.seed_superuser()
        self.stdout.write('Data seeded successfully.')

    def seed_lang(self):
        lang_data = [
            {'lang_id': 1, 'lang_code': 'en', 'lang_name': 'English'},
            {'lang_id': 2, 'lang_code': 'uk', 'lang_name': 'Ukrainian'},
        ]
        for _ in lang_data:
            Language.objects.update_or_create(**_)

    def seed_rewards(self):
        rewards_data = [
            {"id": 1, "name": "Referral reached Rank 1", "amount": 0.0009765625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 2, "name": "Referral reached Rank 2", "amount": 0.001953125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 3, "name": "Referral reached Rank 3", "amount": 0.00390625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 4, "name": "Referral reached Rank 4", "amount": 0.0078125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 5, "name": "Referral reached Rank 5", "amount": 0.015625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 6, "name": "Referral reached Rank 6", "amount": 0.03125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 7, "name": "Referral reached Rank 7", "amount": 0.0625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 8, "name": "Referral reached Rank 8", "amount": 0.125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 9, "name": "Referral reached Rank 9", "amount": 0.25, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 10, "name": "Referral reached Rank 10", "amount": 0.5, "reward_type": Reward.RewardType.G_TOKEN},
            {"id": 11, "name": "Gold Reward", "amount": 1_000, "reward_type": Reward.RewardType.GOLD},
            {"id": 12, "name": "Multiplier Reward", "amount": 2, "reward_type": Reward.RewardType.MULTIPLIER},
            # Add more rewards as needed
        ]
        for reward_data in rewards_data:
            Reward.objects.update_or_create(**reward_data)

    def seed_ranks(self):
        ranks_data = [
            {"id": 1, "name": "Ельфійський ліс", "description": "Starting rank", "gold_required": 10_000, "inviter_reward": Reward.objects.get(id=1)},
            {"id": 2, "name": "Вічна мерзлота", "description": "Intermediate rank", "gold_required": 30_000, "inviter_reward": Reward.objects.get(id=2)},
            # Add more ranks as needed
        ]
        for rank_data in ranks_data:
            Rank.objects.update_or_create(**rank_data)

    def seed_tasks(self):
        tasks_data = [
            {"id": 1, "name": "Subscribe to Channel", "text": "Subscribe to our channel.",
             "task_type": Task.TaskType.ch_sub, "completion_number": 1, "initial": True},
            {"id": 2, "name": "Invite 5 friends", "text": "Invite a friend to join.",
             "task_type": Task.TaskType.inv_fren, "completion_number": 5, "initial": False},
            # Add more tasks as needed
        ]
        for task_data in tasks_data:
            Task.objects.update_or_create(**task_data)

    def seed_energy_levels(self):
        energy_levels_data = [
            {"id": 1, "name": "Energy Level 1", "level": 1, "amount": 100},
            {"id": 2, "name": "Energy Level 2", "level": 2, "amount": 500},
            # Add more energy levels as needed
        ]
        for energy_level_data in energy_levels_data:
            EnergyLevel.objects.update_or_create(**energy_level_data)

    def seed_multiplier_levels(self):
        multiplier_levels_data = [
            {"id": 1, "name": "Multiplier Level 1", "level": 1, "amount": 1},
            {"id": 2, "name": "Multiplier Level 2", "level": 2, "amount": 4},
            # Add more multiplier levels as needed
        ]
        for multiplier_level_data in multiplier_levels_data:
            MultiplierLevel.objects.update_or_create(**multiplier_level_data)

    def seed_passive_income_levels(self):
        passive_income_levels_data = [
            {"id": 1, "name": "Passive Income Level 1", "level": 1, "amount": 100},
            {"id": 2, "name": "Passive Income Level 2", "level": 2, "amount": 200},
            # Add more passive income levels as needed
        ]
        for passive_income_level_data in passive_income_levels_data:
            PassiveIncomeLevel.objects.update_or_create(**passive_income_level_data)

    def seed_links(self):
        links = [
            {"url": os.environ.get("TG_CHANNEL"), "task": Task.objects.get(id=1)}
        ]
        for data in links:
            Link.objects.update_or_create(url=data['url'], defaults=data)

    def seed_users(self):
        users = [
            {'tg_id': 123568, 'tg_username': 'test_mister', 'firstname': 'mister', 'lastname': 'test',
             'interface_lang': Language.objects.get(lang_id=1), 'last_login': now()},
            {'tg_id': 123456, 'tg_username': 'test_miss', 'firstname': 'miss', 'lastname': 'test',
             'interface_lang': Language.objects.get(lang_id=1), 'last_login': now()},
            {'tg_id': 123457, 'tg_username': 'test_none', 'firstname': 'miss', 'lastname': 'test',
             'interface_lang': Language.objects.get(lang_id=1), 'last_login': now()},
        ]
        for data in users:
            User.objects.update_or_create(tg_id=data['tg_id'], defaults=data)

    def seed_user_data(self):
        user_data = [
            {'user_id': User.objects.get(tg_id=123568), 'character_gender': 0, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': Rank.objects.get(id=1),
             'click_multiplier': MultiplierLevel.objects.get(id=1), 'energy': EnergyLevel.objects.get(id=1),
             'current_energy': EnergyLevel.objects.get(id=1).amount,
             'passive_income': PassiveIncomeLevel.objects.get(id=1)},
            {'user_id': User.objects.get(tg_id=123456), 'character_gender': 1, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': Rank.objects.get(id=1),
             'click_multiplier': MultiplierLevel.objects.get(id=1), 'energy': EnergyLevel.objects.get(id=1),
             'current_energy': EnergyLevel.objects.get(id=1).amount,
             'passive_income': PassiveIncomeLevel.objects.get(id=1)},
            {'user_id': User.objects.get(tg_id=123457), 'character_gender': None, 'gold_balance': 0, 'g_token': 0,
             'last_visited': now(), 'rank': Rank.objects.get(id=1),
             'click_multiplier': MultiplierLevel.objects.get(id=1), 'energy': EnergyLevel.objects.get(id=1),
             'current_energy': EnergyLevel.objects.get(id=1).amount,
             'passive_income': PassiveIncomeLevel.objects.get(id=1)},
        ]
        for data in user_data:
            UserData.objects.update_or_create(user_id=data['user_id'], defaults=data)

    def seed_superuser(self):
        users = [
            {'tg_id': os.environ.get("ADMIN_TG_ID"), 'tg_username': os.environ.get("ADMIN_USERNAME"),
             'password': os.environ.get("ADMIN_PASSWORD")},
        ]
        for data in users:
            User.objects.create_superuser(tg_id=data['tg_id'], tg_username=data['tg_username'], password=data['password'])
