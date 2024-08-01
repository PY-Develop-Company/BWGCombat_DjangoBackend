# Generated by Django 5.0.6 on 2024-07-17 11:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0012_alter_userdata_blocked_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='blocked_until',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]