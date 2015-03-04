# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_enumfield.db.fields
import django_enumfield.enum
import athon.enums


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0006_auto_20150304_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='unit',
            field=django_enumfield.db.fields.EnumField(default=1, enum=athon.enums.Unit, choices=[(1, django_enumfield.enum.Value(b'METRIC', 1, 'Metric', athon.enums.Unit)), (2, django_enumfield.enum.Value(b'US', 2, 'US', athon.enums.Unit))]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='weight',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
