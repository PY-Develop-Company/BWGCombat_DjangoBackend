# Generated by Django 5.0.6 on 2024-08-01 09:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0022_remove_stagetemplate_has_keylock_stage_has_keylock'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerSocialTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=64)),
                ('name_de', models.CharField(max_length=64)),
                ('name_fr', models.CharField(max_length=64)),
                ('name_ru', models.CharField(max_length=64)),
                ('name_uk', models.CharField(max_length=64)),
                ('name_zh', models.CharField(max_length=64)),
                ('description_en', models.TextField()),
                ('description_de', models.TextField()),
                ('description_fr', models.TextField()),
                ('description_ru', models.TextField()),
                ('description_uk', models.TextField()),
                ('description_zh', models.TextField()),
                ('link', models.CharField(max_length=1024)),
                ('reward_amount', models.BigIntegerField()),
                ('is_partner', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': '9.1_Out_Rank_Tasks model',
            },
        ),
        migrations.DeleteModel(
            name='SocialMedia',
        ),
        migrations.RenameModel(
            old_name='CompletedSocialTasks',
            new_name='CompletedPartnersSocialTasks',
        ),
        migrations.AddField(
            model_name='completedpartnerssocialtasks',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levels_app.partnersocialtasks'),
        ),
    ]
