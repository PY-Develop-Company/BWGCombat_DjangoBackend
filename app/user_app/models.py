from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.timezone import now

from levels_app.models import Rank, Stage


class CustomUserManager(BaseUserManager):
    def _create_user(self, tg_username, tg_id, password, **extra_fields):
        if not tg_username or not tg_id:
            raise ValueError("You haven't passed tg_username and/or tg_id")
        user = self.model(tg_username=tg_username, tg_id=tg_id, **extra_fields)
        if password:
            user.set_password(password)
        else:
            print('ми потрапляємо сюди навіть коли пароль додався на попередньому етапі')
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, tg_username=None, tg_id=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(tg_username, tg_id, None, **extra_fields)

    def create_staff_member(self, tg_username=None, tg_id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(tg_username, tg_id, password, **extra_fields)

    def create_superuser(self, tg_username=None, tg_id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self._create_user(tg_username, tg_id, password, **extra_fields)


class Language(models.Model):
    lang_id = models.IntegerField(blank=False, primary_key=True)
    lang_code = models.CharField(blank=False, unique=True, max_length=2)
    lang_name = models.CharField(blank=True, unique=False, default='', max_length=100)

    def __str__(self) -> str:
        return self.lang_code


class User(AbstractBaseUser, PermissionsMixin):
    tg_id = models.BigIntegerField(blank=False, primary_key=True)
    tg_username = models.CharField(blank=False, unique=True, max_length=255)
    firstname = models.CharField(blank=True, null=True, default='', max_length=255)
    lastname = models.CharField(blank=True, null=True, default='', max_length=255)
    interface_lang = models.ForeignKey(Language, to_field='lang_code', default='en', on_delete=models.SET_DEFAULT)
    email = None

    is_active = models.BooleanField(default=True)
    is_superuser = None
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'tg_username'

    REQUIRED_FIELDS = ['tg_id']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_full_name(self):
        return str(self.firstname) + ' ' + str(self.lastname) if self.firstname else self.tg_username


class UserData(models.Model):
    user_id = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE
    )
    gold_balance = models.BigIntegerField(null=False, default=0)
    g_token = models.FloatField(null=False, default=0)
    last_visited = models.DateTimeField(null=False, default=now)
    rank_id = models.OneToOneField(
        Rank, null=True, blank=False, on_delete=models.CASCADE, default=None
    )
    stage_id = models.OneToOneField(
        Stage, null=True, blank=False, on_delete=models.CASCADE, default=None
    )

    def add_gold_coins(self, coins: int):
        self.gold_balance += int(coins)
        self.save()

    def set_gold_coins(self, coins: int):
        self.gold_balance = int(coins)
        self.save()

    def remove_gold_coins(self, coins: int):
        self.gold_balance -= int(coins)
        self.save()

    def add_g_token_coins(self, coins: int):
        self.g_token += int(coins)
        self.save()

    def set_g_token_coins(self, coins: int):
        self.g_token = int(coins)
        self.save()

    def remove_g_token_coins(self, coins: int):
        self.g_token -= int(coins)
        self.save()


class Fren(models.Model):
    fren_tg_id = models.BigIntegerField(blank=False, primary_key=True)
    inviter_tg_id = models.ForeignKey(User, on_delete=models.CASCADE)
