# Generated by Django 5.0.6 on 2024-06-25 09:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_app", "0011_userdata_energy_regeneration"),
    ]

    operations = [
        migrations.AddField(
            model_name="userdata",
            name="bot_multitap",
            field=models.BigIntegerField(default=100, help_text="coins per hour"),
        ),
    ]
