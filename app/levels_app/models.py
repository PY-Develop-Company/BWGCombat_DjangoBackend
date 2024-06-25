from django.db import models
from django.utils.translation import gettext_lazy as _


class Rank(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )
    next_rank = models.OneToOneField('self', related_name='next_rank_from_rank', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.name}"


class Stage(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    rank_id = models.ForeignKey(Rank, null=True, blank=False, on_delete=models.CASCADE)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )
    tasks_id = models.ManyToManyField('Task')
    next_stage = models.ForeignKey('self', related_name='next_stage_from_stage', null=True, blank=True, on_delete=models.DO_NOTHING)
    next_rank = models.ForeignKey('Rank', related_name='next_rank_from_stage', null=True, blank=True, on_delete=models.DO_NOTHING)

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

    class RewardType(models.TextChoices):
        GOLD = '1', _("Gold")
        GOLD_PER_CLICK = '2', _("Gold_per_click")
        G_TOKEN = '3', _("G_Token")

    name = models.CharField(max_length=200, blank=False, null=False)
    amount = models.BigIntegerField(null=False)
    reward_type = models.CharField(null=True, choices=RewardType, default=RewardType.GOLD)

    def __str__(self):
        return f"{self.name}"
