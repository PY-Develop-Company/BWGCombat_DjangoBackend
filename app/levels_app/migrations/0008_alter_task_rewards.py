# Generated by Django 5.0.6 on 2024-06-28 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0007_remove_task_amount_remove_task_reward_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='rewards',
            field=models.ManyToManyField(to='levels_app.reward'),
        ),
    ]