# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0005_auto_20150303_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='metric',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='weight',
        ),
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
