from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, tg_username, tg_id, password, **extra_fields):
        if not tg_username or not tg_id:
            raise ValueError("You haven't passed tg_username and/or tg_id")
        user = self.model(tg_username=tg_username, tg_id=tg_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, tg_username=None, tg_id=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(tg_username, tg_id, None, **extra_fields)

    def create_staff_member(self, tg_username=None, tg_id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(tg_username, tg_id, password, **extra_fields)

    def create_superuser(self, tg_username=None, tg_id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(tg_username, tg_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    tg_id = models.BigIntegerField(blank=False, unique=True, primary_key=True)
    tg_username = models.CharField(blank=False, unique=True, max_length=255)
    firstname = models.CharField(blank=True, default='', max_length=255)
    lastname = models.CharField(blank=True, default='', max_length=255)
    email = None

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'tg_username'
    ID_FIELD = 'tg_id'

    REQUIRED_FIELDS = ['tg_id']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return str(self.firstname) + ' ' + str(self.lastname) if self.firstname else self.tg_username[1:]

