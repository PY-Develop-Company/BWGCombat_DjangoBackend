# Generated by Django 5.0.6 on 2024-07-02 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0002_alter_energylevel_next_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='next_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.stage'),
        ),
    ]
