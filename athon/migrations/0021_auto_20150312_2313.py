# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0020_activitydetails_pace'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisetype',
            name='body_weight',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercisetype',
            name='weighted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
