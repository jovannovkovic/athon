# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0017_auto_20150311_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='time',
        ),
    ]
