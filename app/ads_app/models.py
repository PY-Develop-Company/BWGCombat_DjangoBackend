from django.db import models
from django.utils.translation import gettext_lazy as _
from user_app.models import Link


class Advert(models.Model):
    name = models.CharField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    link = models.ForeignKey(Link, null=False, blank=False, on_delete=models.CASCADE)
    image_path = models.FilePathField(path='./media/ads', unique=True, null=False, blank=False, default='/ad1')
