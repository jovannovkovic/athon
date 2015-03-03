# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0004_remove_athletehistory_sport'),
    ]

    operations = [
        migrations.RenameField(
            model_name='athletehistory',
            old_name='sport1',
            new_name='sport',
        ),
    ]
