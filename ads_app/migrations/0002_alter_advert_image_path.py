# Generated by Django 5.0.6 on 2024-07-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='image_path',
            field=models.FilePathField(default='ad1', path='./media/ads/', unique=True),
        ),
    ]
