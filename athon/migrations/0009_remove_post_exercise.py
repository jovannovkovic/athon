# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0008_post_exercise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='exercise',
        ),
    ]
