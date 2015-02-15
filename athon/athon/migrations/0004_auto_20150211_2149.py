# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0003_auto_20150211_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athonuser',
            name='athlete_history',
            field=models.ManyToManyField(to='athon.AthleteHistory', null=True, blank=True),
            preserve_default=True,
        ),
    ]
