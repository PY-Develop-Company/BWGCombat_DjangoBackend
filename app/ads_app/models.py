from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from user_app.models import Link, User
from levels_app.models import Reward


class Advert(models.Model):
    class Meta:
        abstract = True

    # class ShowPlace(models.TextChoices):
    #     BANNER = "1", _("Banner")
    #     FAIRY = "2", _("Fairy")
    #     CHEST = "3", _("Chest")

    class Region(models.TextChoices):
        EUROPE = "1", _("Europe")
        INDIA = "2", _("India")
        CENTRAL_ASIA = "3", _("Central Asia")
        USA_CANADA = "4", _("USA and Canada")
        LATIN_AMERICA = "5", _("Latin America")
        AFRICA = "6", _("Africa")

    name = models.CharField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    link = models.ForeignKey(Link, null=False, blank=False, on_delete=models.CASCADE)
    relevant_region = models.CharField(choices=Region, default=1, null=False, blank=False)
    file_path = models.FilePathField(path='./media/ads/', unique=True, null=False, blank=False, default='ad1')
    # show_place = models.CharField(choices=ShowPlace, default=1, null=False, blank=False)

    # def is_fullscreen(self):
    #     return True if self.show_place in (self.ShowPlace.FAIRY,
    #                                        self.ShowPlace.CHEST) else False


class BannerAdvert(Advert):
    pass


class FullscreenAdvert(Advert):
    view_gold_reward = models.ForeignKey(Reward, null=True, blank=True, default=None, on_delete=models.SET_NULL,
                                         related_name="ads_with_gold_reward")
    view_gnome_reward = models.ForeignKey(Reward, null=True, blank=True, default=None, on_delete=models.SET_NULL,
                                          related_name="ads_with_gnome_reward")
    gnome_probability = models.FloatField(null=False, blank=False, default=0.0002)
    is_video = models.BooleanField(default=False)


class AdView(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    advert = models.ForeignKey(FullscreenAdvert, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    is_clicked = models.BooleanField(default=False)
    seconds_before_click = models.FloatField(null=True, blank=True, default=None)
    is_fairy = models.BooleanField(default=False)
