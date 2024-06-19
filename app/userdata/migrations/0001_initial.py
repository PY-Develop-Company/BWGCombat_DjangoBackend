# Generated by Django 4.1.13 on 2024-06-19 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('amount', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.rank')),
                ('reward_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.reward')),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gold_balance', models.BigIntegerField(default=0)),
                ('g_token', models.FloatField(default=0)),
                ('last_visited', models.DateTimeField(default=django.utils.timezone.now)),
                ('rank_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='userdata.rank')),
                ('stage_id', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='userdata.stage')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('text', models.TextField(null=True)),
                ('reward_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.reward')),
            ],
        ),
        migrations.AddField(
            model_name='rank',
            name='reward_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.reward'),
        ),
    ]
