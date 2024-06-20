from django.db import models
from django.contrib.auth.models import User  ### need to import CustomUser
from django.utils.timezone import now

# Create your models here.


class UserData(models.Model):
    user_id = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE
    )  ### replace User to CustomUser later
    gold_balance = models.BigIntegerField(null=False, default=0)
    g_token = models.FloatField(null=False, default=0)
    last_visited = models.DateTimeField(null=False, default=now)
    rank_id = models.OneToOneField(
        "Rank", null=False, blank=False, on_delete=models.CASCADE
    )
    stage_id = models.OneToOneField(
        "Stage", null=False, blank=False, on_delete=models.CASCADE
    )


class Rank(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Stage(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    rank_id = models.ForeignKey(Rank, null=True, blank=False, on_delete=models.CASCADE)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField(null=True, blank=False)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Reward(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    amount = models.BigIntegerField(null=False)

    def __str__(self):
        return f"{self.name}"
