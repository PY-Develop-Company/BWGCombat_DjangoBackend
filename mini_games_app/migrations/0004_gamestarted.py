# Generated by Django 5.0.6 on 2024-08-09 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_games_app', '0003_remove_levelinfo_amount_attempted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameStarted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('tg_user_id', models.IntegerField()),
                ('level_name', models.CharField()),
            ],
        ),
    ]
