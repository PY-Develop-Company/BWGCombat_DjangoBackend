# Generated by Django 5.0.6 on 2024-08-07 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0026_remove_rank_init_energy_and_more'),
        ('user_app', '0016_alter_userstasks_task'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TaskRoutes',
        ),
    ]
