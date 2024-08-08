from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from user_app.models import User
from links_app.models import Link, BasicLinkClick
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
    view_max_gold_reward = models.ForeignKey(Reward, null=True, blank=True, default=None, on_delete=models.SET_NULL,
                                             related_name="ads_with_max_gold_reward")
    view_min_gold_reward = models.ForeignKey(Reward, null=True, blank=True, default=None, on_delete=models.SET_NULL,
                                             related_name="ads_with_min_gold_reward")
    view_gnome_reward = models.ForeignKey(Reward, null=True, blank=True, default=None, on_delete=models.SET_NULL,
                                          related_name="ads_with_gnome_reward")
    gnome_probability = models.FloatField(null=False, blank=False, default=0.0002)
    is_video = models.BooleanField(default=False)


class AdView(models.Model):
    user = models.ForeignKey("user_app.User", on_delete=models.DO_NOTHING)
    advert = models.ForeignKey(FullscreenAdvert, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    is_clicked = models.BooleanField(default=False)
    seconds_before_click = models.FloatField(null=True, blank=True, default=None)
    is_fairy = models.BooleanField(default=False)


class FullscreenAdLinkClick(BasicLinkClick):
    link = None  # the link is accessible via  advert
    advert = models.ForeignKey(FullscreenAdvert, on_delete=models.CASCADE, null=False, blank=False)


class BannerAdLinkClick(BasicLinkClick):
    link = None  # the link is accessible via  advert
    advert = models.ForeignKey(BannerAdvert, on_delete=models.CASCADE, null=False, blank=False)


class AdSet(models.Model):
    banner = models.ForeignKey(BannerAdvert, on_delete=models.SET_NULL, null=True, blank=True)
    fullscreen = models.ForeignKey(FullscreenAdvert, on_delete=models.SET_NULL, null=True, blank=True)
    current_clicks_number = models.BigIntegerField(default=0, null=False, blank=False)
    clicks_goal = models.BigIntegerField(default=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_goal_reached = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['banner'],
                condition=Q(banner__isnull=False),
                name='unique_banner'
            ),
            UniqueConstraint(
                fields=['fullscreen'],
                condition=Q(fullscreen__isnull=False),
                name='unique_fullscreen'
            ),
        ]

    def __str__(self):
        return f"AdSet(banner={self.banner}, fullscreen={self.fullscreen})"

    def disable_if_goal_reached(self):
        if not self.is_active or not self.clicks_goal:
            return False
        if self.current_clicks_number >= self.clicks_goal:
            self.is_goal_reached = True
            self.is_active = False
            self.save()
            return True
        else:
            return False

