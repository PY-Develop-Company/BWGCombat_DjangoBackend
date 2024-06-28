# Generated by Django 5.0.6 on 2024-06-24 13:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("levels_app", "0002_reward_reward_type"),
        ("user_app", "0009_merge_0005_merge_20240624_1047_0008_userdata_energy"),
    ]

    operations = [
        migrations.CreateModel(
            name="User_tasks",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="levels_app.task",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
