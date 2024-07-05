from django.db import models
from user_app.models import User
from django.utils import timezone


class Asset(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)


class Swap(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING)
    asset_1 = models.ForeignKey(Asset, null=False, blank=False, on_delete=models.DO_NOTHING,
                                related_name='swaps_giving')
    asset_2 = models.ForeignKey(Asset, null=False, blank=False, on_delete=models.DO_NOTHING,
                                related_name='swaps_receiving')
    fee = models.FloatField(null=False, blank=False, default=0.0)
    amount_1 = models.FloatField(null=False, blank=False, default=0.0)
    amount_2 = models.FloatField(null=False, blank=False, default=0.0)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (f"{self.user} gave {self.amount_1} of {self.asset_1} and received {self.amount_2} of {self.asset_2} "
                f"with fee of {self.fee} G-tokens at {self.time}")


class Transfer(models.Model):
    user_1 = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING,
                               related_name='transfers_giving')
    user_2 = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING,
                               related_name='transfers_receiving')
    asset = models.ForeignKey(Asset, null=False, blank=False, on_delete=models.DO_NOTHING)
    fee = models.FloatField(null=False, blank=False, default=0.0)
    amount = models.FloatField(null=False, blank=False, default=0.0)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (f"{self.user_1} gave {self.amount} of {self.asset} to {self.user_2} "
                f"with fee of {self.fee} G-tokens at {self.time}")


class ExchangeRate(models.Model):
    asset_1 = models.ForeignKey(Asset, null=False, blank=False, on_delete=models.DO_NOTHING,
                                related_name='rates_sell')
    asset_2 = models.ForeignKey(Asset, null=False, blank=False, on_delete=models.DO_NOTHING,
                                related_name='rates_buy')
    rate = models.FloatField(null=False, blank=False, default=1.0)
