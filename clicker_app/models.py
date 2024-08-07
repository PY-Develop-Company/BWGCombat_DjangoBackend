from django.db import models
from django.core.validators import MinValueValidator


class UpgradeLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    next_level = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.name}  {self.level}  {self.amount}'

    class Meta:
        abstract = True


class EnergyBalanceUpgradeLevel(UpgradeLevel):
    pass


class MulticlickUpgradeLevel(UpgradeLevel):
    pass
