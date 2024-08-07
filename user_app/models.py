from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from levels_app.models import Rank, TaskTemplate, TaskRoute, Reward, Stage
import tg_connection


class CustomUserManager(BaseUserManager):
    def _create_user(self, tg_username, tg_id, password, **extra_fields):
        if not tg_username or not tg_id:
            raise ValueError("You haven't passed tg_username and/or tg_id")
        user = self.model(tg_username=tg_username, tg_id=tg_id, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def update_or_create(self, defaults=None, **kwargs):

        instance, created = super().update_or_create(defaults=defaults, **kwargs)
        try:
            password = defaults['password']
        except KeyError:
            instance.set_unusable_password()
        else:
            instance.set_password(password)
        finally:
            instance.save(update_fields=['password'])

        return instance, created

    def create_user(self, tg_username=None, tg_id=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(tg_username, tg_id, None, **extra_fields)

    def create_staff_member(
        self, tg_username=None, tg_id=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(tg_username, tg_id, password, **extra_fields)

    def create_superuser(
        self, tg_username=None, tg_id=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(tg_username, tg_id, password, **extra_fields)


class Language(models.Model):
    lang_code = models.CharField(unique=True, max_length=2)
    lang_name = models.CharField(blank=True, unique=False, default="", max_length=100)

    def __str__(self) -> str:
        return self.lang_code


class User(AbstractBaseUser, PermissionsMixin):
    tg_id = models.BigIntegerField(blank=False, primary_key=True)
    tg_username = models.CharField(null=True, blank=False, unique=True, max_length=255)
    firstname = models.CharField(blank=True, null=True, default="", max_length=255)
    lastname = models.CharField(blank=True, null=True, default="", max_length=255)
    interface_lang = models.ForeignKey(
        Language,
        to_field="lang_code",
        null=True,
        default="en",
        on_delete=models.SET_DEFAULT,
    )
    email = None

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "tg_username"
    REQUIRED_FIELDS = ["tg_id"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.tg_id}  {self.tg_username or ''}"


class UserData(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 0, 'Male'
        FEMALE = 1, 'Female'

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    character_gender = models.IntegerField(null=True, blank=True, default=0, choices=Gender.choices)

    gold_balance = models.BigIntegerField(default=0)
    g_token = models.FloatField(default=0)

    last_visited = models.DateTimeField(default=now)

    rank = models.ForeignKey(Rank, null=True, on_delete=models.SET_NULL, default=1)
    current_stage = models.ForeignKey(Stage, null=True, default=1, on_delete=models.SET_NULL)

    multiclick = models.IntegerField(default=2)
    energy_regeneration = models.IntegerField(default=1)
    energy_balance = models.IntegerField(default=100)
    current_energy = models.IntegerField(default=0)
    gnome_amount = models.IntegerField(default=0)

    is_vip = models.BooleanField(default=False)

    # language = models.ForeignKey(Language, to_field='lang_code', null=True, on_delete=models.SET_DEFAULT, default='en')
    visual_effects = models.BooleanField(default=True)
    general_volume = models.PositiveSmallIntegerField(default=50)
    effects_volume = models.PositiveSmallIntegerField(default=50)
    music_volume = models.PositiveSmallIntegerField(default=50)

    has_key = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(default=now)

    def add_gold_coins(self, coins: int):
        self.gold_balance += int(coins)

    def set_gold_coins(self, coins: int):
        self.gold_balance = int(coins)

    def remove_gold_coins(self, coins: int):
        self.gold_balance -= int(coins)

    def add_g_token_coins(self, coins: float):
        if not isinstance(coins, float):
            coins = float(coins)
        self.g_token += coins
        self.g_token = round(self.g_token, 12)

    def set_g_token_coins(self, coins: float):
        if not isinstance(coins, float):
            coins = float(coins)
        self.g_token = coins
        self.g_token = round(self.g_token, 12)

    def remove_g_token_coins(self, coins: float):
        if not isinstance(coins, float):
            coins = float(coins)
        self.g_token -= coins
        self.g_token = round(self.g_token, 12)

    def set_multiplier(self, multiplier: int):
        self.multiclick = multiplier

    def add_multiplier(self, multiplier: int):
        self.multiclick += multiplier

    def add_energy(self, energy: int):
        self.energy_balance += energy

    def set_energy(self, energy: int):
        self.energy_balance = energy
        
    def add_gnomes(self, amount: int = 1):
        self.gnome_amount += amount

    def set_gnomes(self, amount: int):
        self.gnome_amount = amount

    def remove_gnomes(self, amount: int):
        self.gnome_amount -= amount

    def set_key(self):
        self.has_key = True

    def set_prisoning(self, amount: int):
        self.blocked_until += now() + datetime.hour(amount)

    def is_referrals_quantity_exceeds(self, expected_quantity):
        user = User.objects.get(tg_id=self.user_id)
        refs_quantity = user.referrals.count()
        return True if refs_quantity >= expected_quantity else False

    async def check_channel_subscription(self, channel_id):
        pass
        # channel_id = 'https://t.me/justforcheckingone'
        # await tg_connection.is_subscribed_to_channel(...)

    def check_link_click(self, link):
        user = User.objects.get(user_id=self.user_id)
        return LinkClick.objects.filter(user=user, link=link).exists()

    def make_vip(self):
        self.is_vip = True
        self.save()

    def revoke_vip(self):
        self.is_vip = False
        self.save()

    def receive_reward(self, reward: Reward):
        reward_amount = int(reward.amount)

        match reward.reward_type:
            case Reward.RewardType.GOLD:
                self.add_gold_coins(reward_amount)
            case Reward.RewardType.G_TOKEN:
                self.add_g_token_coins(reward_amount)

            case Reward.RewardType.MULTICKLICK:
                self.add_multiplier(reward_amount)
            case Reward.RewardType.ENERGY_BALANCE:
                self.add_energy(reward_amount)

            case Reward.RewardType.KEY:
                self.set_key()
            case Reward.RewardType.GNOME:
                self.add_gnomes(reward_amount)
            case Reward.RewardType.JAIL:
                self.set_prisoning(reward_amount)
            
            case _:
                return "No such reward type"

    def __str__(self):
        return f'{self.user_id} {self.last_visited}'


class UsersTasks(models.Model): 
    class Status(models.TextChoices):
        UNAVAILABLE = "0", _("Unavailable")
        IN_PROGRESS = "1", _("In progress")
        NOT_CLAIMED = "4", _("Not claimed")
        CLAIMED = "2", _("Claimed")
        EXPIRED = "3", _("Expired")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(TaskRoute, on_delete=models.CASCADE)
    rewards = models.ManyToManyField(Reward, blank=True)
    completion_time = models.DateTimeField(null=True, blank=True, default=None)

    status = models.CharField(null=False, blank=False, choices=Status, default=Status.UNAVAILABLE)

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self) -> str:
        return f"{self.id} {self.user.tg_username} {self.task.template.name}"
    
    def get_user_subtasks(self, user):
        sub = self.task.subtasks.values_list('id', flat=True)
        return UsersTasks.objects.filter(task__in=sub, user=user)


class Fren(models.Model):
    fren_tg = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    inviter_tg = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="referrals"
    )

    class Meta:
        unique_together = ("fren_tg", "inviter_tg")

    def clean(self):
        if self.fren_tg == self.inviter_tg:
            raise ValidationError("You cannot add yourself as a friend.")

        # Check if the reverse relationship already exists
        if Fren.objects.filter(
            inviter_tg=self.fren_tg, fren_tg=self.inviter_tg
        ).exists():
            raise ValidationError("This friendship already exists in reverse.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Fren, self).save(*args, **kwargs)


class Link(models.Model):
    url = models.URLField(unique=True)
    task = models.ForeignKey(TaskTemplate, null=True, on_delete=models.SET_NULL, default=None)


class LinkClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, to_field='url', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
