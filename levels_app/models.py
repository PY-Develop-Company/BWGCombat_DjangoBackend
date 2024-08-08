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

    swap_limit = models.IntegerField(null=False, default=10)  # in G-tokens

    next_rank = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_all_tasks(self, user_data: int):
        from user_app.models import UsersTasks

        stages = self.get_all_stages()
        tasks = TaskRoutes.objects.filter(stage__in=stages) \
            .exclude(id__in=UsersTasks.objects.filter(user=user_data.user).values_list('task_id', flat=True)).distinct()

        return tasks

    def get_empty_chests(self, user_data):
        from user_app.models import UsersTasks

        stages = self.get_all_stages()
        tasks = TaskRoutes.objects.filter(stage__in=stages, template__in=TaskTemplate.objects.filter(task_type=TaskTemplate.TaskType.buy_chest))\
        .exclude(id__in=UsersTasks.objects.filter(user=user_data.user).values_list('task_id', flat=True)).distinct()

        return tasks

    def get_not_chest_tasks(self, user_data):
        from user_app.models import UsersTasks

        stages = self.get_all_stages()
        tasks = TaskRoutes.objects.filter(stage__in=stages).exclude(template__task_type=TaskTemplate.TaskType.buy_chest) \
            .exclude(id__in=UsersTasks.objects.filter(user=user_data.user).values_list('task_id', flat=True)).distinct()

        return tasks

    def get_all_stages(self):
        stages = []
        curr_stage = self.init_stage

        while curr_stage:
            stages.append(curr_stage)
            curr_stage = curr_stage.next_stage
        return stages

    class Meta:
        verbose_name_plural = ('1_Rank model')


class StageTemplate(models.Model):
    name = models.CharField(max_length=255, default='none')
    task_with_keys = models.ManyToManyField('TaskRoutes', blank=True)
    keys_amount = models.IntegerField(default=1)
    jail_amount = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = ('2.1_StageTemplate models')


class Stage(models.Model):
    name = models.CharField(max_length=255)
    next_stage = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    initial_task = models.ForeignKey('TaskRoutes', null=True, on_delete=models.SET_NULL, related_name='ini_task')
    has_keylock = models.BooleanField(default=True)
    tasks = models.ManyToManyField('TaskRoutes', related_name='stage')
    stage_template = models.ForeignKey('StageTemplate', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name} -> {self.next_stage}'

    def get_empty_chests(self, user_data):
        from user_app.models import UsersTasks

        chest_tasks = self.tasks.filter(template__task_type=TaskTemplate.TaskType.buy_chest)
        empty_chests = chest_tasks.exclude(
            id__in=UsersTasks.objects.filter(user=user_data.user).values_list('task_id', flat=True))

        return empty_chests

    def get_not_chest_tasks(self, user_data):
        from user_app.models import UsersTasks

        not_chest = self.tasks.exclude(template__task_type=TaskTemplate.TaskType.buy_chest)
        empty_chests = not_chest.exclude(
            id__in=UsersTasks.objects.filter(user=user_data.user).values_list('task_id', flat=True))

        return empty_chests

    class Meta:
        verbose_name_plural = ('2.2_Stage model')


class TaskTemplate(models.Model):
    class TaskType(models.TextChoices):
        ch_sub = "1", _("sub to channel")
        inv_fren = "2", _("invite friend")
        earn_gold = "3", _("earn N amount of gold")
        buy_energy = "4", _("buy energy")
        buy_multiclick = "5", _("buy pickaxe")
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
    parent = models.ForeignKey('self', blank=True, on_delete=models.SET_NULL, null=True, related_name='subtasks')
    initial = models.BooleanField(default=False)

    def get_subtasks(self):
        return self.subtasks.all()

    def __str__(self) -> str:
        return f'{self.template} + ({self.coord_x},{self.coord_y})'

    class Meta:
        verbose_name_plural = ('4_TaskRoutes model')


class Reward(models.Model):
    class RewardType(models.TextChoices):
        GOLD = "1", _("Add gold")
        MULTIPLIER = "2", _("Increase gold multiplier")
        G_TOKEN = "3", _("Add G token")
        ENERGY_BALANCE = "4", _("Replenish energy")
        KEY = '5', _('Key')
        GNOME = '6', _('Gnome')
        JAIL = '7', _('Jail')

    name = models.CharField(max_length=200, unique=True)
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


class PartnersButtonTypes(models.Model):
    name_en = models.CharField(max_length=64, blank=False, default="Register")
    name_de = models.CharField(max_length=64, blank=False, default="Register")
    name_fr = models.CharField(max_length=64, blank=False, default="Register")
    name_ru = models.CharField(max_length=64, blank=False, default="Register")
    name_uk = models.CharField(max_length=64, blank=False, default="Register")
    name_zh = models.CharField(max_length=64, blank=False, default="Register")


class PartnersTasks(models.Model):
    name = models.CharField(max_length=64)
    button_type = models.ForeignKey(PartnersButtonTypes, on_delete=models.SET_DEFAULT, default=0)
    link = models.CharField(max_length=1024)
    reward_amount = models.BigIntegerField()


class SocialTasks(models.Model):
    name_en = models.CharField(max_length=64, blank=False)
    name_de = models.CharField(max_length=64, blank=False)
    name_fr = models.CharField(max_length=64, blank=False)
    name_ru = models.CharField(max_length=64, blank=False)
    name_uk = models.CharField(max_length=64, blank=False)
    name_zh = models.CharField(max_length=64, blank=False)
    link = models.CharField(max_length=1024, null=False, blank=False)
    reward_amount = models.BigIntegerField(null=False, blank=False)


class CompletedSocialTasks(models.Model):
    user = models.ForeignKey("user_app.User", on_delete=models.CASCADE)
    task = models.ForeignKey(SocialTasks, on_delete=models.CASCADE)


class CompletedPartnersTasks(models.Model):
    user = models.ForeignKey("user_app.User", on_delete=models.CASCADE)
    task = models.ForeignKey(PartnersTasks, on_delete=models.CASCADE)
