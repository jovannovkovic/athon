# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0002_sport'),
    ]

    operations = [
        migrations.AddField(
            model_name='athletehistory',
            name='sport1',
            field=models.ForeignKey(blank=True, to='athon.Sport', null=True),
            preserve_default=True,
        ),
    ]
