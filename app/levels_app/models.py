from django.db import models
from django.utils.translation import gettext_lazy as _


class Rank(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )
    next_rank = models.OneToOneField(
        "self",
        related_name="next_rank_from_rank",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    fist_stage = models.ForeignKey('Stage', null = True, on_delete=models.DO_NOTHING, default=None)

    def __str__(self) -> str:
        return f"{self.name}"


class Stage(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    rank_id = models.ForeignKey(Rank, null=True, blank=False, on_delete=models.CASCADE)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )
    tasks_id = models.ManyToManyField("Task")
    next_stage = models.ForeignKey(
        "self",
        related_name="next_stage_from_stage",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    class TaskType(models.TextChoices):
        ch_sub = "1", _("sub to channel")
        inv_fren = "2", _("invite friend")
        earn_gold = "3", _("earn N amount of gold")
        buy_energy = "4", _("buy energy")
        gnome_empl = "5", _("Gnome employment(buying)")
        pick_upg = "6", _("upgrade pickaxe to earn more gold per click")
        buy_char = "7", _("buy character to improve passive income")

    name = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField(null=True, blank=False)
    amount = models.IntegerField(null = True)
    task_type = models.CharField(
        null=False, choices=TaskType, default=TaskType.buy_energy
    )
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Reward(models.Model):
    class RewardType(models.TextChoices):
        GOLD = "1", _("Gold")
        GOLD_PER_CLICK = "2", _("Gold_per_click")
        G_TOKEN = '3', _("G_Token")
        
        GOLD_AND_PICKAXE = '4', _("add gold per click + pickaxe upgrade")
        ENERGY_BALANCE =  '5', _('energy balance ')
        ENERGY_AND_GOLD_PER_CLICK  ="6", _("energy balance + add gold per click")
        ADD_PASSIVE_INCOME = "7", _("add  passive income")

    name = models.CharField(max_length=200, blank=False, null=False)
    amount = models.BigIntegerField(null=False)
    reward_type = models.CharField(
        null=True, choices=RewardType, default=RewardType.GOLD
    )

    def __str__(self):
        return f"{self.name}"
