from django.db import models
from django.utils.translation import gettext_lazy as _


class Rank(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1023, default='No description')
    gold_required = models.BigIntegerField(null=True, blank=True, default=10_000)

    inviter_reward = models.ForeignKey(
        "Reward", null=True, blank=False, on_delete=models.DO_NOTHING
    )
    init_stage = models.ForeignKey('Stage', null=True, on_delete=models.SET_NULL)

    init_energy = models.ForeignKey('MaxEnergyLevel', null=False, on_delete=models.SET_DEFAULT, default=1)
    init_multiplier = models.ForeignKey('MulticlickLevel', null=False, on_delete=models.SET_DEFAULT, default=1)
    init_energy_regeneration = models.IntegerField(null=False, default=1)

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = ('1_Rank model')


class StageTemplate(models.Model):
    task_with_keys = models.ManyToManyField('TaskRoutes')
    keys_amount = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = ('2.1_StageTemplate models')


class Stage(models.Model):
    name = models.CharField(max_length=255)
    next_stage = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    initial_task = models.ForeignKey('TaskRoutes', null=True, on_delete=models.SET_NULL, related_name='ini_task')
    tasks = models.ManyToManyField('TaskRoutes', related_name='stage')

    def __str__(self) -> str:
        return f'{self.name} -> {self.next_stage}'

    class Meta:
        verbose_name_plural = ('2.2_Stage model')



class TaskTemplate(models.Model):
    class TaskType(models.TextChoices):
        ch_sub = "1", _("sub to channel")
        inv_fren = "2", _("invite friend")
        earn_gold = "3", _("earn N amount of gold")
        buy_energy = "4", _("buy energy")
        buy_multicklick = "5", _("buy pickaxe")
        buy_chest = "6", _("buy chest")
        road = "7", _("buy road")

    name = models.CharField(max_length=255)
    text = models.TextField(null=True)
    task_type = models.CharField(choices=TaskType, default=TaskType.buy_chest)
    completion_number = models.BigIntegerField(null=True, blank=True)

    rewards = models.ManyToManyField("Reward")
    price = models.BigIntegerField(default=0, null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = ('3_TaskTemplate model')

class TaskRoutes(models.Model):
    coord_x = models.IntegerField(default=0, null=False)
    coord_y = models.IntegerField(default=0, null=False)
    template = models.ForeignKey(TaskTemplate, blank=False, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, on_delete=models.SET_NULL, null=True)
    initial = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.template.name} + ({self.coord_x},{self.coord_y})'


    class Meta:
        verbose_name_plural = ('4_TaskRoutes model')


class Reward(models.Model):
    class RewardType(models.TextChoices):
        GOLD = "1", _("Add gold")
        MULTIPLIER = "2", _("Increase gold multiplier")
        G_TOKEN = "3", _("Add G token")
        ENERGY_BALANCE = "4", _("Replenish energy")
        PASSIVE_INCOME = "5", _("Improve passive income")

    name = models.CharField(max_length=200)
    amount = models.FloatField()
    reward_type = models.CharField(null=True, choices=RewardType, default=RewardType.GOLD)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = ('5_Reward model')


class MaxEnergyLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    amount = models.IntegerField()
    next_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name}  {self.level}  {self.amount}'
    
    class Meta:
        verbose_name_plural = ('6_Energy model')


class MulticlickLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    amount = models.IntegerField()
    next_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name}  {self.level}  {self.amount}'
    
    class Meta:
        verbose_name_plural = ('7_Multiplier model')


class PassiveIncomeLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    amount = models.IntegerField()
    next_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name}  {self.level}  {self.amount}'
    
    class Meta:
        verbose_name_plural = ('8_PassiveIncome model')
    

class SocialMedia(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    link = models.CharField(max_length=1024, null=False, blank=False)
    reward_amount = models.BigIntegerField(null=False, blank=False)
    # maybe add imageField?
    is_partner = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = ('9.1_Out_Rank_Tasks model')


class CompletedSocialTasks(models.Model):
    user = models.ForeignKey('user_app.User', null=False, on_delete=models.CASCADE)
    task = models.ForeignKey(SocialMedia, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = ('9.2_Completed_Out_Rank_Tasks model')

