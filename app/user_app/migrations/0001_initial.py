# Generated by Django 5.0.6 on 2024-07-02 10:58

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('levels_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('lang_id', models.IntegerField(primary_key=True, serialize=False)),
                ('lang_code', models.CharField(max_length=2, unique=True)),
                ('lang_name', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('tg_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('tg_username', models.CharField(max_length=255, null=True, unique=True)),
                ('firstname', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('interface_lang', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='user_app.language', to_field='lang_code')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='LinkClick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.link', to_field='url')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gold_balance', models.BigIntegerField(default=0)),
                ('g_token', models.FloatField(default=0)),
                ('last_visited', models.DateTimeField(default=django.utils.timezone.now)),
                ('energy_regeneration', models.IntegerField(default=1)),
                ('click_multiplier', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Click_level', to='levels_app.multiplierlevel')),
                ('energy', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.energylevel')),
                ('passive_income', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passive_level', to='levels_app.passiveincomelevel')),
                ('rank_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.rank')),
                ('stage_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='levels_app.stage')),
            ],
        ),
        migrations.CreateModel(
            name='UsersTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levels_app.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'task')},
            },
        ),
        migrations.CreateModel(
            name='Fren',
            fields=[
                ('fren_tg', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('inviter_tg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('fren_tg', 'inviter_tg')},
            },
        ),
    ]
