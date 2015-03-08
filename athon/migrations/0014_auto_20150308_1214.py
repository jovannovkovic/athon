# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0013_auto_20150308_1211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='duration',
            new_name='time',
        ),
        migrations.AlterField(
            model_name='exercise',
            name='post',
            field=models.ForeignKey(related_name='exercises', blank=True, to='athon.Post', null=True),
            preserve_default=True,
        ),
    ]
