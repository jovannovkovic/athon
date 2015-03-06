# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0011_auto_20150306_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitytype',
            name='hint',
            field=models.CharField(max_length=125, null=True, verbose_name=b'Npr. Create training with rounds', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name='posts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
