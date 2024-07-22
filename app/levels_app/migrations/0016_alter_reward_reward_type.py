# Generated by Django 5.0.6 on 2024-07-16 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0015_alter_reward_name_alter_reward_reward_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='reward_type',
            field=models.CharField(choices=[('1', 'Add gold'), ('2', 'Increase gold multiplier'), ('3', 'Add G token'), ('4', 'Replenish energy'), ('5', 'Improve passive income'), ('6', 'Key'), ('7', 'Gnome')], default='1', null=True),
        ),
    ]
