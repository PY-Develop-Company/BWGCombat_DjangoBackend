# Generated by Django 5.0.6 on 2024-07-04 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0002_alter_reward_amount'),
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='energy',
            new_name='max_energy',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='character_gender',
            field=models.IntegerField(blank=True, choices=[(0, 'Male'), (1, 'Female')], default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='rank',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.rank'),
        ),
    ]
