# Generated by Django 5.0.6 on 2024-07-15 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0013_alter_stagetemplate_task_with_keys'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='next_rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.rank'),
        ),
    ]
