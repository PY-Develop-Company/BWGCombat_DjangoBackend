from django.core.management.base import BaseCommand
from levels_app.models import Rank, Task, Reward, EnergyLevel, MultiplierLevel, PassiveIncomeLevel
from user_app.models import User, Language, UserData
from django.utils.timezone import now

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
        self.seed_users()
        # self.seed_user_data()
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
            {"name": "Gold Reward", "amount": 1_000, "reward_type": Reward.RewardType.GOLD},
            {"name": "Multiplier Reward", "amount": 2, "reward_type": Reward.RewardType.MULTIPLIER},
            # Add more rewards as needed
        ]
        for reward_data in rewards_data:
            Reward.objects.update_or_create(**reward_data)
        
    def seed_ranks(self):
        ranks_data = [
            {"id": 1, "name": "Ельфійський ліс", "description": "Starting rank", "gold_required": 10_000},
            {"id": 2, "name": "Вічна мерзлота", "description": "Intermediate rank", "gold_required": 30_000},
            # Add more ranks as needed
        ]
        for rank_data in ranks_data:
            Rank.objects.update_or_create(**rank_data)
        
    def seed_tasks(self):
        tasks_data = [
            {"name": "Subscribe to Channel", "text": "Subscribe to our channel.", "task_type": Task.TaskType.ch_sub, "completion_number": 1, "initial": True},
            {"name": "Invite 5 friends Friend", "text": "Invite a friend to join.", "task_type": Task.TaskType.inv_fren, "completion_number": 5, "initial": False},
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

    def seed_users(self):
        users = [
            {'tg_id': 123568, 'tg_username': 'test_mister', 'firstname': 'mister', 'lastname': 'test', 'interface_lang': Language.objects.get(lang_id=1), 'last_login': now()},
            {'tg_id': 123456, 'tg_username': 'test_miss', 'firstname': 'misis', 'lastname': 'test', 'interface_lang': Language.objects.get(lang_id=1), 'last_login': now()},
        ]
        for _ in users:
            User.objects.update_or_create(**_)

