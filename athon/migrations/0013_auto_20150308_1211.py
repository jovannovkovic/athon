# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0012_auto_20150306_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='activity',
            new_name='title',
        ),
    ]
