# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0019_post_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitydetails',
            name='pace',
            field=models.CharField(max_length=125, null=True, blank=True),
            preserve_default=True,
        ),
    ]
