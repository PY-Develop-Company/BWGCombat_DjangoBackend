# Generated by Django 5.0.6 on 2024-08-08 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links_app', '0002_linkmodel_data_alter_linkmodel_link_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Status',
        ),
        migrations.RemoveField(
            model_name='userlinkmodel',
            name='claim_timestamp',
        ),
    ]
