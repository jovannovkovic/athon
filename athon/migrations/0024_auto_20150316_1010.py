# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import athon.enums
import django_enumfield.enum
import django_enumfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('athon', '0023_auto_20150315_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deadline', models.DateTimeField()),
                ('description', models.TextField()),
                ('post', models.ForeignKey(related_name='challenge', to='athon.Post')),
                ('subscribers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChallengeResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response', django_enumfield.db.fields.EnumField(default=1, enum=athon.enums.ChallengeResponse, choices=[(1, django_enumfield.enum.Value(b'ACEPTED', 1, 'Acepted', athon.enums.ChallengeResponse)), (2, django_enumfield.enum.Value(b'REJECTED', 2, 'Rejected', athon.enums.ChallengeResponse)), (3, django_enumfield.enum.Value(b'PENDING', 3, 'Pending', athon.enums.ChallengeResponse))])),
                ('date_responded', models.DateTimeField(null=True, blank=True)),
                ('result', models.FloatField(default=0)),
                ('challenge', models.ForeignKey(related_name='responses', to='athon.Challenge')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChallengeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125, null=True, verbose_name=b'Npr. DO, ili SPORT', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='challenge',
            name='type',
            field=models.ForeignKey(blank=True, to='athon.ChallengeType', null=True),
            preserve_default=True,
        ),
    ]
