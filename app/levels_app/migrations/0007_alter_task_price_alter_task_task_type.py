# Generated by Django 5.0.6 on 2024-07-10 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0006_rank_init_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='price',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('1', 'sub to channel'), ('2', 'invite friend'), ('3', 'earn N amount of gold'), ('4', 'buy energy'), ('5', 'buy pickaxe'), ('6', 'buy chest'), ('7', 'buy road')], default='6'),
        ),
    ]