# Generated by Django 5.0.6 on 2024-08-08 08:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0008_banneradlinkclick_fullscreenadlinkclick'),
        ('links_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='banneradvert',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='links_app.link'),
        ),
        migrations.AlterField(
            model_name='fullscreenadvert',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='links_app.link'),
        ),
        migrations.AddField(
            model_name='banneradlinkclick',
            name='advert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads_app.banneradvert'),
        ),
        migrations.AddField(
            model_name='banneradlinkclick',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='links_app.link', to_field='url'),
        ),
        migrations.AddField(
            model_name='banneradlinkclick',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fullscreenadlinkclick',
            name='advert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads_app.fullscreenadvert'),
        ),
        migrations.AddField(
            model_name='fullscreenadlinkclick',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='links_app.link', to_field='url'),
        ),
        migrations.AddField(
            model_name='fullscreenadlinkclick',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]