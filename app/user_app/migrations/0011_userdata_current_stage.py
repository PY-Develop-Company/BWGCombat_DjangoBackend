# Generated by Django 5.0.6 on 2024-07-17 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0019_alter_reward_reward_type'),
        ('user_app', '0010_userdata_effects_volume_userdata_general_volume_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='current_stage',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.stage'),
        ),
    ]