# Generated by Django 5.0.6 on 2024-07-05 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0001_initial'),
        ('user_app', '0003_link_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='task',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.task'),
        ),
    ]