from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Rank
from .models import UserData


@receiver(post_save, sender=User)
def add_user_data_record(sender, instance, created, **kwargs):
    if created:
        initial_rank = Rank.objects.first()
        user_data = UserData.objects.create(user_id=instance, 
                                            rank=initial_rank,
                                            max_energy_amount=initial_rank.init_energy.amount,
                                            multiclick_amount=initial_rank.init_multiplier.amount)
        user_data.save()
        return user_data