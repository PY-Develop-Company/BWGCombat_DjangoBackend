# Generated by Django 5.0.6 on 2024-06-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0003_alter_reward_reward_type'),
        ('user_app', '0011_merge_0006_merge_20240625_1013_0010_user_tasks'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_tasks',
            new_name='UsersTasks',
        ),
        migrations.AlterField(
            model_name='user',
            name='tg_username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]