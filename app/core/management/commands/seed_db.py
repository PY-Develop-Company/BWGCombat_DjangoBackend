import os

from ads_app.models import Advert
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from levels_app.models import Rank, TaskTemplate, TaskRoutes, Reward, MaxEnergyLevel, MulticlickLevel, PassiveIncomeLevel, SocialMedia, CompletedSocialTasks, StageTemplate, Stage
from user_app.models import User, Language, UserData, CustomUserManager, Link, Fren
from exchanger_app.models import Asset, ExchangePair
import os
from django.db import transaction


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
            {"id":1, "name": "KEY", "amount": 1, "reward_type": Reward.RewardType.KEY},
            {"id":2, "name": "Gnome", "amount": 1, "reward_type": Reward.RewardType.GNOME},
            {"id":3, "name": "Jail", "amount": 12, "reward_type": Reward.RewardType.GNOME},
            {"id":4, "name": "Referral reached Rank 1", "amount": 0.0009765625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":5, "name": "Referral reached Rank 2", "amount": 0.001953125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":6, "name": "Referral reached Rank 3", "amount": 0.00390625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":7, "name": "Referral reached Rank 4", "amount": 0.0078125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":8, "name": "Referral reached Rank 5", "amount": 0.015625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":9, "name": "Referral reached Rank 6", "amount": 0.03125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":10, "name": "Referral reached Rank 7", "amount": 0.0625, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":11, "name": "Referral reached Rank 8", "amount": 0.125, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":12, "name": "Referral reached Rank 9", "amount": 0.25, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":13, "name": "Referral reached Rank 10", "amount": 0.5, "reward_type": Reward.RewardType.G_TOKEN},
            {"id":14, "name": "gold +1000", "amount": 1000, "reward_type": Reward.RewardType.GOLD},
            {"id":15, "name": "gold -1000", "amount": -1000, "reward_type": Reward.RewardType.GOLD},
            {"id":16, "name": "energy +50", "amount": 50, "reward_type": Reward.RewardType.ENERGY_BALANCE},
            {"id":17, "name": "multiclick +2", "amount": 2, "reward_type": Reward.RewardType.MULTIPLIER},
            {"id":18, "name": "multiclick +10", "amount": 10, "reward_type": Reward.RewardType.MULTIPLIER},
            # Add more rewards as needed
        ]
        for reward_data in rewards_data:
            Reward.objects.update_or_create(name=reward_data['name'], defaults=reward_data)

    def seed_ranks(self):
        ranks_data = [
            {"id": 1, "name": "Ельфійський ліс", "description": "Starting rank", "gold_required": 10000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 1"), 'init_stage_id':1, 'next_rank_id':2},
            {"id": 2, "name": "Вічна мерзлота", "description": "Intermediate rank", "gold_required": 30000,
             "inviter_reward": Reward.objects.get(name="Referral reached Rank 2"),  'init_stage_id':2, 'next_rank_id':3},
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
            next_rank = rank_data.pop('next_rank_id', None)
            rank,_ = Rank.objects.update_or_create(name=rank_data['name'], defaults=rank_data)
            rank.next_rank_id = next_rank
            rank.save()


    def seed_stage_templates(self):
        stage_temp_data = [
            {"id": 1, "name": "1_stage_1_rank_tmp", "keys_amount": 0, "jail_amount":0},
            {"id": 2, "name": "1_stage_2_rank_tmp", "keys_amount": 0, "jail_amount":0},
        ]
        for rank_data in stage_temp_data:
            StageTemplate.objects.update_or_create(id=rank_data['id'], defaults=rank_data)

    def seed_stage(self):
        stage_data = [
            {"id": 1, "name": "1_stage_1_rank", "initial_task_id":1, "tasks":[1,2], "stage_template_id":1},
            {"id": 2, "name": "1_stage_2_rank", "initial_task_id":3, "tasks":[x for x in range(3,11)], "stage_template_id":1},
        ]
        for stage_data in stage_data:
            st,_ = Stage.objects.update_or_create(id=stage_data['id'], defaults={"name":stage_data['name'], "initial_task_id":stage_data['initial_task_id'], "stage_template_id":stage_data['stage_template_id']})
            st.tasks.add(*stage_data['tasks'])
            st.save()




    @transaction.atomic
    def seed_task_templates(self):
        desc = "Buy chest and get chance to get extra gnome"
        task_templates_data = [
            { "id":1, "name": "Subscribe to Channel",   "text": "Subscribe to our channel.",    "task_type": TaskTemplate.TaskType.ch_sub,          "completion_number": 1, "price": 0,     "rewards": [Reward.objects.get(id=16), Reward.objects.get(id=17)]},
            { "id":2, "name": "Invite 1 friends",       "text": "Invite a friend to join.",     "task_type": TaskTemplate.TaskType.inv_fren,        "completion_number": 1, "price": 0,     "rewards": [Reward.objects.get(id=16), Reward.objects.get(id=18) ]},
            { "id":3, "name": "chest_1000",             "text": f"{desc}",                      "task_type": TaskTemplate.TaskType.buy_chest,       "completion_number": 1, "price": 1000,  "rewards": [Reward.objects.get(id=11), Reward.objects.get(id=12), Reward.objects.get(id=2)]},
            { "id":4, "name": "Upgrade pickaxe",        "text": "Earn more gold with 1 click",  "task_type": TaskTemplate.TaskType.buy_multicklick, "completion_number": 0, "price": 2000,  "rewards": [Reward.objects.get(id=17) ]},
            { "id":5, "name": "Upgrade energy",         "text": "Buy more energy",              "task_type": TaskTemplate.TaskType.buy_energy,      "completion_number": 0, "price": 2000,  "rewards": [Reward.objects.get(id=16)]},
            # Add more task templates as needed
        ]

        for task_template_data in task_templates_data:
            if task_template_data["id"] in [1,2]:
                self.tasks_1_stage.append(task_template_data)
            rewards = task_template_data.pop("rewards", [])
            task_template, created = TaskTemplate.objects.update_or_create(
                name=task_template_data['name'],
                defaults=task_template_data
            )
            if created or task_template.rewards.count() != len(rewards):
                task_template.rewards.set(rewards)
            task_template.save()


    @transaction.atomic
    def seed_task_routes(self):
        task_routes_data = [
            {"id":1,"coord_x": 0,"coord_y": 0,"template_id": 1,"parent":None,"initial": True},
            {"id":2,"coord_x": 0,"coord_y": -1,"template_id": 2,  "parent_id": 1,"initial": False},
            # 2 rank 1 stage
            {"id":  3, "coord_x":  0,  "coord_y":  0 ,  "template_id": 5,  "parent_id": None, "initial": True},
            {"id":  4, "coord_x":  -1, "coord_y": 0,    "template_id": 4,  "parent_id": 3,    "initial": False},
            {"id":  5, "coord_x":  -2, "coord_y":  0,   "template_id": 3,  "parent_id": 4,    "initial": False,},
            {"id":  6, "coord_x":  1,  "coord_y": 0,    "template_id": 3,  "parent_id": 1,    "initial": False,},
            {"id":  7, "coord_x":  0,  "coord_y":  -1,  "template_id": 5,  "parent_id": 1,    "initial": False,},
            {"id":  8, "coord_x":  -1, "coord_y": -1,   "template_id": 4,  "parent_id": 7,    "initial": False},
            {"id":  9, "coord_x":  0,  "coord_y":  -2,  "template_id": 5,  "parent_id": 7,    "initial": False,},
            {"id": 10, "coord_x":  -1, "coord_y": -2,   "template_id": 2,  "parent_id": 9,    "initial": False,},
        ]
    
        for task_route_data in task_routes_data:
            task_route, created = TaskRoutes.objects.update_or_create(
                id = task_route_data['id'],
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
             "link": Link.objects.get(id=1), "image_path": "azino777.jfif"}
        ]
        for data in ads:
            Advert.objects.update_or_create(id=data['id'], defaults=data)
