# Generated by Django 5.0.6 on 2024-07-15 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels_app', '0003_alter_taskroutes_subtasks'),
    ]

    operations = [
        migrations.CreateModel(
            name='StageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keys_amount', models.IntegerField(default=1)),
                ('task_with_keys', models.ManyToManyField(to='levels_app.taskroutes')),
            ],
        ),
    ]