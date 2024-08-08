from django.db import models

from levels_app.models import TaskTemplate
# from user_app.models import User
# from ads_app.models import FullscreenAdvert, BannerAdvert


# Create your models here.
class Link(models.Model):
    url = models.URLField(unique=True)
    task = models.ForeignKey(TaskTemplate, null=True, on_delete=models.SET_NULL, default=None)


class BasicLinkClick(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey("user_app.User", on_delete=models.CASCADE)
    link = models.ForeignKey(Link, to_field='url', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class LinkClick(BasicLinkClick):
    pass

