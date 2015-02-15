# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('athon', '0002_auto_20150206_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, verbose_name='activation key')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='fallowusers',
            old_name='fallowing_user',
            new_name='followed_user',
        ),
        migrations.RenameField(
            model_name='fallowusers',
            old_name='user',
            new_name='follower',
        ),
    ]
