# Generated by Django 5.0.6 on 2024-07-15 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0010_rename_subtasks_taskroutes_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='stage_template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.stagetemplate'),
        ),
    ]
