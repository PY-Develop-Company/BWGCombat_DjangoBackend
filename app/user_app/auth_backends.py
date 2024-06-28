from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, tg_id=None, password=None):
        try:
            user = self.user_class.objects.get(tg_id=tg_id)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, tg_id):
        try:
            return self.user_class.objects.get(tg_id=tg_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, "_user_class"):
            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split(".", 2))
            if not self._user_class:
                raise ImproperlyConfigured("Could not get custom user model")
        return self._user_class
