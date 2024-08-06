# Generated by Django 5.0.6 on 2024-08-05 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0006_remove_fullscreenadvert_view_gold_reward_and_more'),
        ('levels_app', '0023_rank_swap_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='fullscreenadvert',
            name='view_max_gold_reward',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ads_with_max_gold_reward', to='levels_app.reward'),
        ),
    ]