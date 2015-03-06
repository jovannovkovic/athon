# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0009_remove_post_exercise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='reps',
        ),
        migrations.AddField(
            model_name='exercise',
            name='post',
            field=models.ForeignKey(related_name='exercise', blank=True, to='athon.Post', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='repetition',
            name='exercise',
            field=models.ForeignKey(blank=True, to='athon.Exercise', null=True),
            preserve_default=True,
        ),
    ]
