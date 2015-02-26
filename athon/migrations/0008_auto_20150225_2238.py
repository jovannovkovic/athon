# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import athon.enums
import uuid_upload_path.storage
import django_enumfield.enum
import django_enumfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('athon', '0007_auto_20150224_2317'),
    ]

    operations = [
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
                ('athlete_history', models.ManyToManyField(to='athon.AthleteHistory', null=True, blank=True)),
                ('follow_users', models.ManyToManyField(related_name='related_to_following', through='athon.FollowUsers', to='athon.Profile')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='athonuser',
            name='athlete_history',
        ),
        migrations.RemoveField(
            model_name='athonuser',
            name='follow_users',
        ),
        migrations.RemoveField(
            model_name='athonuser',
            name='user',
        ),
        migrations.AlterField(
            model_name='followusers',
            name='followed_user',
            field=models.ForeignKey(related_name='followers', to='athon.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='followusers',
            name='follower',
            field=models.ForeignKey(related_name='following', to='athon.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.OneToOneField(related_name='posts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='AthonUser',
        ),
    ]
