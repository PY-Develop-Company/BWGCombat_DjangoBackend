import os

from ads_app.models import Advert
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from exchanger_app.models import Asset, ExchangePair
from levels_app.models import Rank, Task, Reward, MaxEnergyLevel, MulticlickLevel, PassiveIncomeLevel, SocialMedia, \
    CompletedSocialTasks
from user_app.models import User, Language, UserData, Link, Fren


class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.seed_energy_levels()
        self.seed_multiplier_levels()
        self.seed_passive_income_levels()

        self.seed_lang()

        self.seed_rewards()
        self.seed_ranks()
        self.seed_tasks()
        self.seed_links()

        self.seed_users()
        self.seed_frens()

        self.seed_social_media()
        self.seed_completed_social_tasks()

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
            {"name": "Referral reached Rank 1", "amount": 0.0009765625, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 2", "amount": 0.001953125, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 3", "amount": 0.00390625, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 4", "amount": 0.0078125, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 5", "amount": 0.015625, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 6", "amount": 0.03125, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 7", "amount": 0.0625, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 8", "amount": 0.125, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 9", "amount": 0.25, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Referral reached Rank 10", "amount": 0.5, "reward_type": Reward.RewardType.G_TOKEN},
            {"name": "Gold Reward", "amount": 1000, "reward_type": Reward.RewardType.GOLD},
            {"name": "Multiplier Reward", "amount": 2, "reward_type": Reward.RewardType.MULTIPLIER},
            # Add more rewards as needed
        ]
        for reward_data in rewards_data:
            Reward.objects.update_or_create(name=reward_data['name'], defaults=reward_data)

    def seed_ranks(self):
        ranks_data = [
            {"id": 1, "name": "Ельфійський ліс", "description": "Starting rank", "gold_required": 10000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 1")},
            {"id": 2, "name": "Вічна мерзлота", "description": "Intermediate rank", "gold_required": 30000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 2")},
            {"id": 3, "name": "Rank 3", "description": "Intermediate rank", "gold_required": 60000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 3")},
            {"id": 4, "name": "Rank 4", "description": "Intermediate rank", "gold_required": 90000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 4")},
            {"id": 5, "name": "Rank 5", "description": "Intermediate rank", "gold_required": 120000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 5")},
            {"id": 6, "name": "Rank 6", "description": "Intermediate rank", "gold_required": 150000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 6")},
            {"id": 7, "name": "Rank 7", "description": "Intermediate rank", "gold_required": 180000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 7")},
            {"id": 8, "name": "Rank 8", "description": "Intermediate rank", "gold_required": 210000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 8")},
            {"id": 9, "name": "Rank 9", "description": "Intermediate rank", "gold_required": 240000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 9")},
            {"id": 10, "name": "Rank 10", "description": "Last rank", "gold_required": 300000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 10")},

            # Add more ranks as needed
        ]
        for rank_data in ranks_data:
            Rank.objects.update_or_create(name=rank_data['name'], defaults=rank_data)

    def seed_tasks(self):
        tasks_data = [
            {"name": "Subscribe to Channel", "text": "Subscribe to our channel.", "task_type": Task.TaskType.ch_sub,
             "completion_number": 1, "is_initial": True},
            {"name": "Invite 5 friends", "text": "Invite a friend to join.", "task_type": Task.TaskType.inv_fren,
             "completion_number": 5, "is_initial": False},
            # Add more tasks as needed
        ]
        for task_data in tasks_data:
            Task.objects.update_or_create(name=task_data['name'], defaults=task_data)

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
            {"url": os.environ.get("TG_CHANNEL"), "task": Task.objects.get(name="Subscribe to Channel")}
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
            {"id": 2, "name": "Gold"}
        ]
        for data in assets:
            Asset.objects.update_or_create(id=data['id'], defaults=data)

    def seed_exchange_pairs(self):
        pairs = [
            {"id": 1, "asset_1": Asset.objects.get(id=1), "asset_2": Asset.objects.get(id=2), "rate": 100_000},
            {"id": 2, "asset_1": Asset.objects.get(id=2), "asset_2": Asset.objects.get(id=1), "rate": 0.00001}
        ]
        for data in pairs:
            ExchangePair.objects.update_or_create(id=data['id'], defaults=data)

    def seed_social_media(self):
        social_medias = [
            {"id": 1, "name": "Facebook", "link": "https://www.facebook.com", "reward_amount": 5000,
             "is_partner": True},
            {"id": 2, "name": "Twitter", "link": "https://www.twitter.com", "reward_amount": 3000, "is_partner": False},
            {"id": 3, "name": "Instagram", "link": "https://www.instagram.com", "reward_amount": 4000,
             "is_partner": True}
        ]
        for data in social_medias:
            SocialMedia.objects.update_or_create(id=data['id'], defaults=data)

    def seed_completed_social_tasks(self):
        tasks = [
            {"id": 1, "user": User.objects.get(tg_id=123456), "task": SocialMedia.objects.get(id=1)},
            {"id": 2, "user": User.objects.get(tg_id=123456), "task": SocialMedia.objects.get(id=2)},
            {"id": 3, "user": User.objects.get(tg_id=123568), "task": SocialMedia.objects.get(id=2)},
        ]
        for data in tasks:
            CompletedSocialTasks.objects.update_or_create(id=data['id'], defaults=data)

    def seed_ads(self):
        ads = [
            {"id": 1, "name": "Azino 777", "description": "Vygravaytie 100000000000000000000 rubley",
             "link": Link.objects.get(id=1), "image_path": "/azino777.jfif"}
        ]
        for data in ads:
            Advert.objects.update_or_create(id=data['id'], defaults=data)
