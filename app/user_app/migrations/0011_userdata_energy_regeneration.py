# Generated by Django 5.0.6 on 2024-06-25 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0010_user_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='energy_regeneration',
            field=models.IntegerField(default=1),
        ),
    ]
