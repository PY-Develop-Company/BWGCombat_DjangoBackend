from django.db import models
from django.utils.translation import gettext_lazy as _
from user_app.models import Link


class Advert(models.Model):
    name = models.CharField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    link = models.ForeignKey(Link, null=False, blank=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="./media/ads", null=True, blank=True, default=None)
