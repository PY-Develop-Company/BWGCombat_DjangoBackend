from django.db import models
from django.utils.translation import gettext_lazy as _


class Rank(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=False, max_length=1023, default='Some text')

    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.DO_NOTHING
    )

    first_stage = models.ForeignKey('Stage', null = True, blank=True, on_delete=models.DO_NOTHING, default=None)

    def __str__(self) -> str:
        return f"{self.name}"


class Stage(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    rank_id = models.ForeignKey(Rank, null=True, blank=False, on_delete=models.CASCADE)
    reward_id = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.DO_NOTHING
    )
    tasks_id = models.ManyToManyField("Task")
    next_stage = models.ForeignKey('self', null = True, blank=True, on_delete=models.SET_NULL)
    


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

    name = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField(null=True, blank=False)
    task_type = models.CharField(
        null=False, choices=TaskType, default=TaskType.buy_energy
    )
    completion_number = models.BigIntegerField(null=True, blank=True)
    rewards = models.ManyToManyField(
        "Reward", blank=False
    )

    def __str__(self) -> str:
        return self.name


class Reward(models.Model):
    class RewardType(models.TextChoices):
        GOLD = "1", _("Add gold")
        MULTIPLIER = "2", _("Increase gold multiplier")
        G_TOKEN = "3", _("Add G token")
        ENERGY_BALANCE = "4", _("Replenish energy")
        PASSIVE_INCOME = "5", _("Improve passive income")

    name = models.CharField(max_length=200, blank=False, null=False)
    amount = models.BigIntegerField(null=False)
    reward_type = models.CharField(null=True, choices=RewardType, default=RewardType.GOLD)

    def __str__(self):
        return f"{self.name}"
    

class EnergyLevel(models.Model):
    id = models.IntegerField(blank=False, null = False, primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    level = models.IntegerField(null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    next_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name}  {self.level}  {self.amount}'

class MultiplierLevel(models.Model):
    id = models.IntegerField(blank=False, null = False, primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    level = models.IntegerField(null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    next_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name}  {self.level}  {self.amount}'

class PassiveIncomeLevel(models.Model):
    id = models.IntegerField(blank=False, null = False, primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    level = models.IntegerField(null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    next_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name}  {self.level}  {self.amount}'
