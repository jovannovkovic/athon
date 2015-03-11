# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0018_remove_post_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
