# Generated by Django 5.0.6 on 2024-07-16 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0018_alter_reward_reward_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='reward_type',
            field=models.CharField(choices=[('1', 'Add gold'), ('2', 'Increase gold multiplier'), ('3', 'Add G token'), ('4', 'Replenish energy'), ('5', 'Key'), ('6', 'Gnome'), ('7', 'Jail')], default='1', null=True),
        ),
    ]