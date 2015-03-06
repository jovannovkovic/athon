# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0010_auto_20150306_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repetition',
            name='exercise',
            field=models.ForeignKey(related_name='reps', blank=True, to='athon.Exercise', null=True),
            preserve_default=True,
        ),
    ]
