# Generated by Django 5.0.6 on 2024-06-28 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0023_link_linkclick'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linkclick',
            old_name='user_id',
            new_name='user',
        ),
    ]
