# Generated by Django 5.0.6 on 2024-06-27 08:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_app", "0018_alter_fren_fren_tg"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fren",
            name="fren_tg",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]