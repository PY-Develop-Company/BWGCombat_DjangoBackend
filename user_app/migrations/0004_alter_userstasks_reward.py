# Generated by Django 5.0.6 on 2024-07-15 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0015_alter_reward_name_alter_reward_reward_type'),
        ('user_app', '0003_remove_userstasks_reward_userstasks_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstasks',
            name='reward',
            field=models.ManyToManyField(blank=True, to='levels_app.reward'),
        ),
    ]