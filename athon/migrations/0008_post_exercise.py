# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0007_auto_20150304_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='exercise',
            field=models.ForeignKey(blank=True, to='athon.Exercise', null=True),
            preserve_default=True,
        ),
    ]
