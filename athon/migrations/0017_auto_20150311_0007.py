# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0016_auto_20150310_2342'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rounds', models.CharField(max_length=125, null=True, blank=True)),
                ('series', models.CharField(max_length=125, null=True, blank=True)),
                ('interval', models.CharField(max_length=125, null=True, blank=True)),
                ('for_time', models.CharField(max_length=125, null=True, blank=True)),
                ('amrap', djorm_pgarray.fields.IntegerArrayField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='post',
            name='info',
        ),
        migrations.DeleteModel(
            name='ActivityTypeInfo',
        ),
        migrations.RemoveField(
            model_name='post',
            name='type',
        ),
        migrations.DeleteModel(
            name='ActivityType',
        ),
        migrations.AddField(
            model_name='post',
            name='activity_details',
            field=models.ForeignKey(default=None, blank=True, to='athon.ActivityDetails', null=True),
            preserve_default=True,
        ),
    ]
