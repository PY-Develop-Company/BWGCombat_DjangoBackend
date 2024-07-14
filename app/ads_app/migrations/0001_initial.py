# Generated by Django 5.0.6 on 2024-07-09 13:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0007_remove_userdata_click_multiplier_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('description', models.TextField(blank=True, null=True)),
                ('img_path', models.FilePathField(max_length=255, path='/ads')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.link')),
            ],
        ),
    ]