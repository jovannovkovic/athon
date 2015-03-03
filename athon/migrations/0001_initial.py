# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_enumfield.db.fields
import django_enumfield.enum
import athon.enums
import uuid_upload_path.storage
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=225, null=True, blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125, null=True, verbose_name=b'Npr. Rounds', blank=True)),
                ('hint', models.CharField(max_length=5, null=True, verbose_name=b'Npr. Create training with rounds', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityTypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=125, null=True, blank=True)),
                ('quantity', models.CharField(max_length=125, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AthleteHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sport', models.CharField(max_length=225, null=True, blank=True)),
                ('from_date', models.IntegerField(null=True, blank=True)),
                ('until_date', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExerciseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125, null=True, blank=True)),
                ('quantity', models.BooleanField(default=False)),
                ('repetition', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow_status', django_enumfield.db.fields.EnumField(default=1, enum=athon.enums.FollowStatus, choices=[(1, django_enumfield.enum.Value(b'FOLLOW', 1, 'Follow', athon.enums.FollowStatus)), (2, django_enumfield.enum.Value(b'FOLLOWING', 2, 'Following', athon.enums.FollowStatus))])),
                ('request_status', models.BooleanField(default=False)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_key', models.CharField(max_length=100, verbose_name='temp_key')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('reset', models.BooleanField(default=False, verbose_name='reset yet?')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'password reset',
                'verbose_name_plural': 'password resets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity', models.CharField(max_length=125, null=True, blank=True)),
                ('activity_name', models.CharField(max_length=225, null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=uuid_upload_path.storage.upload_to, blank=True)),
                ('duration', models.TimeField(null=True, blank=True)),
                ('status', models.CharField(max_length=300, null=True, blank=True)),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hidden', models.BooleanField(default=False)),
                ('info', models.ForeignKey(default=None, blank=True, to='athon.ActivityTypeInfo', null=True)),
                ('type', models.ForeignKey(default=None, blank=True, to='athon.ActivityType', null=True)),
                ('user', models.OneToOneField(related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', django_enumfield.db.fields.EnumField(default=1, enum=athon.enums.Gender, choices=[(1, django_enumfield.enum.Value(b'MALE', 1, 'Male', athon.enums.Gender)), (2, django_enumfield.enum.Value(b'FEMALE', 2, 'Female', athon.enums.Gender))])),
                ('birthday', models.DateField(null=True, blank=True)),
                ('hometown', models.CharField(max_length=225, null=True, blank=True)),
                ('metric', models.BooleanField(default=False)),
                ('profile_photo', models.ImageField(null=True, upload_to=uuid_upload_path.storage.upload_to, blank=True)),
                ('is_public_profile', models.BooleanField(default=True)),
                ('height', models.CharField(max_length=10, null=True, blank=True)),
                ('weight', models.CharField(max_length=10, null=True, blank=True)),
                ('following_number', models.PositiveIntegerField(default=0)),
                ('followers_number', models.PositiveIntegerField(default=0)),
                ('follow_users', models.ManyToManyField(related_name='related_to_following', through='athon.FollowUsers', to='athon.Profile')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, verbose_name='activation key')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repetition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveSmallIntegerField(default=0, null=True, blank=True)),
                ('repetition', models.PositiveSmallIntegerField(default=0, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125, null=True, verbose_name=b'Npr. Kilogrami', blank=True)),
                ('hint', models.CharField(max_length=5, null=True, verbose_name=b'Npr. kg', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='repetition',
            name='unit',
            field=models.ForeignKey(blank=True, to='athon.Unit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='followusers',
            name='followed_user',
            field=models.ForeignKey(related_name='followers', to='athon.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='followusers',
            name='follower',
            field=models.ForeignKey(related_name='following', to='athon.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercisetype',
            name='unit',
            field=models.ForeignKey(blank=True, to='athon.Unit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='reps',
            field=models.ManyToManyField(to='athon.Repetition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='type',
            field=models.ForeignKey(to='athon.ExerciseType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athletehistory',
            name='profile',
            field=models.ForeignKey(related_name='athlete_histories', blank=True, to='athon.Profile', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='achievement',
            name='athlete_history',
            field=models.ForeignKey(related_name='achievements', blank=True, to='athon.AthleteHistory', null=True),
            preserve_default=True,
        ),
    ]
