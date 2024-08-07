from django.db import models
from django.core.validators import MinValueValidator


class UpgradeLevel(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.name}  {self.level}'

    class Meta:
        abstract = True


class EnergyBalanceUpgradeLevel(UpgradeLevel):
    pass


class MulticlickUpgradeLevel(UpgradeLevel):
    pass
