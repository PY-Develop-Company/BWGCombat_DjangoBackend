# Generated by Django 5.0.6 on 2024-07-31 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0013_alter_userdata_blocked_until'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='is_vip',
            field=models.BooleanField(default=False),
        ),
    ]