from django.db import models

from tg_connection import is_subscribed_to_channel


class LinkModel(models.Model):
    class LinkType(models.TextChoices):
        TELEGRAM_CHANEL = "TELEGRAM_CHANEL"
        TELEGRAM_OTHER = "TELEGRAM_OTHER"
        OTHER = "OTHER"

    url = models.CharField(max_length=255)
    link_type = models.CharField(choices=LinkType, default=LinkType.OTHER)
    data = models.CharField(max_length=255, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.url} {self.link_type}"

    async def check_completion(self, user):
        match self.link_type:
            case self.LinkType.TELEGRAM_CHANEL:
                res = await is_subscribed_to_channel(user.tg_id, self.data)
                if res:
                    UserLinkModel.objects.create(user=user, link=self)
                return res
            case self.LinkType.OTHER | self.LinkType.TELEGRAM_OTHER:
                return True
            case _:
                raise Exception(f"Unknown link type: {self.link_type}")


class UserLinkModel(models.Model):
    user = models.ForeignKey("user_app.User", on_delete=models.CASCADE)
    link = models.ForeignKey(LinkModel, on_delete=models.CASCADE)

    complete_timestamp = models.DateTimeField(auto_now_add=True)
