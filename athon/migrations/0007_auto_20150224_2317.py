# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid_upload_path.storage


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0006_passwordreset'),
    ]

    operations = [
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
                ('user', models.OneToOneField(related_name='shares', to='athon.AthonUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repetition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('repetition', models.PositiveSmallIntegerField(null=True, blank=True)),
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
            model_name='exercisetype',
            name='unit',
            field=models.ForeignKey(blank=True, to='athon.Unit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_type',
            field=models.ForeignKey(to='athon.ExerciseType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='repetition',
            field=models.ManyToManyField(to='athon.Repetition'),
            preserve_default=True,
        ),
    ]
