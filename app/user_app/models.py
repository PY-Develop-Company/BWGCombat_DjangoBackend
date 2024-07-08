from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from levels_app.models import Rank, Task, Reward, MulticlickLevel, MaxEnergyLevel, PassiveIncomeLevel


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
    lang_id = models.IntegerField(primary_key=True)
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
        all_language_codes = Language.objects.values_list('lang_code', flat=True)
        if 'en' not in all_language_codes:
            english = Language.objects.create(lang_id=1, lang_code='en', lang_name='English')
            english.save()
        super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.tg_id}  {self.tg_username or ''}"


class UserData(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 0, 'Male'
        FEMALE = 1, 'Female'

    user_id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    character_gender = models.IntegerField(null=True, blank=True, default=0, choices=Gender.choices)

    gold_balance = models.BigIntegerField(default=0)
    g_token = models.FloatField(default=0)

    last_visited = models.DateTimeField(default=now)

    rank = models.ForeignKey(Rank, null=True, on_delete=models.SET_NULL, default=1)

    multiclick_level = models.ForeignKey(MulticlickLevel, null=True, blank=True, default=1, on_delete=models.SET_NULL, related_name='Click_level')
    energy_regeneration = models.IntegerField(default=1)
    max_energy_level = models.ForeignKey(MaxEnergyLevel, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    current_energy = models.IntegerField(default=0)

    passive_income_level = models.ForeignKey(PassiveIncomeLevel, null=True, blank=True, default=1, on_delete=models.SET_NULL, related_name='passive_level')

    def add_gold_coins(self, coins: int):
        self.gold_balance += int(coins) * self.multiclick_level.amount

    def set_gold_coins(self, coins: int):
        self.gold_balance = int(coins)

    def remove_gold_coins(self, coins: int):
        self.gold_balance -= int(coins)

    def add_g_token_coins(self, coins: int):
        self.g_token += int(coins)

    def set_g_token_coins(self, coins: int):
        self.g_token = int(coins)

    def remove_g_token_coins(self, coins: int):
        self.g_token -= int(coins)

    def increase_multiplier_level(self, levels_to_increase: int):
        for __ in range(levels_to_increase):
            self.click_multiplier = self.multiclick_level.next_level

    def increase_energy_level(self, levels_to_increase: int):
        for __ in range(levels_to_increase):
            self.energy = self.max_energy_level.next_level

    def increase_passive_income_level(self, levels_to_increase: int):
        for __ in range(levels_to_increase):
            self.passive_income = self.passive_income_level.next_level

    def is_referrals_quantity_exceeds(self, expected_quantity):
        user = User.objects.get(tg_id=self.user_id)
        refs_quantity = user.referrals.count()
        return True if refs_quantity >= expected_quantity else False

    def check_channel_subscription(self, link):
        pass

    def check_link_click(self, link):
        user = User.objects.get(user_id=self.user_id)
        return LinkClick.objects.filter(user=user, link=link).exists()

    def receive_reward(self, reward: Reward):
        """
        GOLD = "1", _("Add gold")
        GOLD_PER_CLICK = "2", _("Increase gold per click multiplier")
        G_TOKEN = '3', _("Add G token")
        ENERGY_BALANCE = '4', _("Replenish energy")
        PASSIVE_INCOME = "5", _("Improve passive income")
        """
        reward_type = int(reward.reward_type)
        reward_amount = int(reward.amount)

        match reward_type:
            case 1:
                self.add_gold_coins(reward_amount)
            case 2:
                self.increase_multiplier_level(reward_amount)
            case 3:
                self.add_g_token_coins(reward_amount)
            case 4:
                self.increase_energy_level(reward_amount)
            case 5:
                self.increase_passive_income_level(reward_amount)
            case _:
                return "No such reward type"

    def __str__(self):
        return f'{self.user_id.tg_id} {self.last_visited}'


class UsersTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True, default=None)
    complete_time = models.DateTimeField(null=True, blank=True, default=None)

    class Status(models.TextChoices):
        UNAVAILABLE = "0", _("Unavailable")
        IN_PROGRESS = "1", _("In progress")
        COMPLETED = "2", _("Completed")
        EXPIRED = "3", _("Expired")
    status = models.CharField(null=False, blank=False, choices=Status, default=Status.UNAVAILABLE)

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self) -> str:
        return self.user.tg_username + self.task.name


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
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL, default=None)


class LinkClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, to_field='url', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
