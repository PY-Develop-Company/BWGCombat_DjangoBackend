# Generated by Django 5.0.6 on 2024-06-23 17:27

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("levels_app", "0001_initial"),
        ("user_app", "0003_merge_20240623_2027"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="interface_lang",
            field=models.ForeignKey(
                default="en",
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="user_app.language",
                to_field="lang_code",
            ),
        ),
        migrations.CreateModel(
            name="UserData",
            fields=[
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("gold_balance", models.BigIntegerField(default=0)),
                ("g_token", models.FloatField(default=0)),
                (
                    "last_visited",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "rank_id",
                    models.OneToOneField(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="levels_app.rank",
                    ),
                ),
                (
                    "stage_id",
                    models.OneToOneField(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="levels_app.stage",
                    ),
                ),
            ],
        ),
    ]