# Generated by Django 5.0.6 on 2024-07-03 11:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0006_remove_stage_next_stage_remove_stage_rank_id_and_more'),
        ('user_app', '0003_merge_20240702_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='rank_id',
            new_name='rank',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='stage_id',
        ),
        migrations.RemoveField(
            model_name='userstasks',
            name='time',
        ),
        migrations.AddField(
            model_name='userstasks',
            name='complete_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='userstasks',
            name='start_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='click_multiplier',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Click_level', to='levels_app.multiplierlevel'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='energy',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.energylevel'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='passive_income',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passive_level', to='levels_app.passiveincomelevel'),
        ),
        migrations.AlterField(
            model_name='userstasks',
            name='status',
            field=models.CharField(choices=[('0', 'Unavailable'), ('1', 'In progress'), ('2', 'Completed'), ('3', 'Expired')], default='0'),
        ),
    ]
