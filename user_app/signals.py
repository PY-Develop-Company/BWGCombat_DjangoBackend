from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Rank
from .models import UserData
from levels_app.utils import place_items


@receiver(post_save, sender=User)
def add_user_data_record(sender, instance, created, **kwargs):
    if created:
        initial_rank = Rank.objects.first()
        user_data = UserData.objects.create(user=instance,
                                            rank=initial_rank,
                                            current_stage=initial_rank.init_stage,
                                            energy_balance=initial_rank.init_energy_balance,
                                            multiclick=initial_rank.init_multiclick,
                                            energy_regeneration=initial_rank.init_energy_regeneration,
                                            current_energy=initial_rank.init_energy_balance)
        user_data.save()
        place_items(user_data, user_data.rank)
        return user_data