# Generated by Django 5.0.6 on 2024-06-26 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0002_reward_reward_type'),
        ('user_app', '0013_merge_20240625_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='rank_id',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.rank'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='stage_id',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.stage'),
        ),
    ]
