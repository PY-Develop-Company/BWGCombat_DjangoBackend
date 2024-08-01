from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from user_app.models import Link, User


class Advert(models.Model):
    class ShowPlace(models.TextChoices):
        BANNER = "1", _("Banner")
        FAIRY = "2", _("Fairy")
        CHEST = "3", _("Chest")

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
    show_place = models.CharField(choices=ShowPlace, default=1, null=False, blank=False)
    relevant_region = models.CharField(choices=Region, default=1, null=False, blank=False)
    is_video = models.BooleanField(default=False)
    file_path = models.FilePathField(path='./media/ads/', unique=True, null=False, blank=False, default='ad1')


class AdView(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
