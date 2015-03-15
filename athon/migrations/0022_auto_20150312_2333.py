# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('athon', '0021_auto_20150312_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedMuscleWork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='athon.ExerciseType')),
                ('tag', models.ForeignKey(related_name='athon_taggedmusclework_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedSynonyms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='athon.ExerciseType')),
                ('tag', models.ForeignKey(related_name='athon_taggedsynonyms_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exercisetype',
            name='exercise_category',
            field=models.ForeignKey(blank=True, to='athon.ExerciseCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercisetype',
            name='muscle_work',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='athon.TaggedMuscleWork', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exercisetype',
            name='synonyms',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='athon.TaggedSynonyms', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
