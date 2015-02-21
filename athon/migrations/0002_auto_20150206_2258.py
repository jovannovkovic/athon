# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_enumfield.db.fields
import django_enumfield.enum
import athon.enums


class Migration(migrations.Migration):
    dependencies = [
        ('athon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=225, null=True, blank=True)),
                ('year', models.DateField(null=True, blank=True)),
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
                ('from_date', models.DateField(null=True, blank=True)),
                ('until_date', models.DateField(null=True, blank=True)),
                ('achievements', models.ManyToManyField(to='athon.Achievement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FallowUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fallow_status', django_enumfield.db.fields.EnumField(default=1, enum=athon.enums.FollowStatus,
                                                                       choices=[(1,
                                                                                 django_enumfield.enum.Value(b'FALLOW',
                                                                                                             1,
                                                                                                             'Fallow',
                                                                                                             athon.enums.FollowStatus)),
                                                                                (2, django_enumfield.enum.Value(
                                                                                    b'FALLOWING', 2, 'Fallowing',
                                                                                    athon.enums.FollowStatus))])),
                ('request_status', models.BooleanField(default=False)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('fallowing_user', models.ForeignKey(related_name='fallowers', to='athon.AthonUser')),
                ('user', models.ForeignKey(related_name='fallowing', to='athon.AthonUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='athonuser',
            name='private_profile',
        ),
        migrations.AddField(
            model_name='athonuser',
            name='athlete_history',
            field=models.ManyToManyField(to='athon.AthleteHistory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athonuser',
            name='fallow_users',
            field=models.ManyToManyField(related_name='related_to_fallowing', through='athon.FallowUsers',
                                         to='athon.AthonUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athonuser',
            name='fallowers_number',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athonuser',
            name='fallowing_number',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athonuser',
            name='height',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athonuser',
            name='is_public_profile',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athonuser',
            name='weight',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
