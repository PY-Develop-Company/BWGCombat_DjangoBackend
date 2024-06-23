from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, UserData


@receiver(post_save, sender=User)
def add_user_data_record(sender, instance, created, **kwargs):
    print('here')
    if created:

        user_data = UserData.objects.create(user_id=instance)
        user_data.save()
        return user_data
