# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0015_exercisetype_synonyms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='hint',
        ),
        migrations.AddField(
            model_name='unit',
            name='imperial',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Npr. mi', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unit',
            name='metric',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Npr. km', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(max_length=125, null=True, verbose_name=b'Npr. Kilometri', blank=True),
            preserve_default=True,
        ),
    ]
