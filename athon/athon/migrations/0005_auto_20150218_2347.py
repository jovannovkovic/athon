# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_enumfield.db.fields
import django_enumfield.enum
import athon.enums


class Migration(migrations.Migration):

    dependencies = [
        ('athon', '0004_auto_20150211_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow_status', django_enumfield.db.fields.EnumField(default=1, enum=athon.enums.FollowStatus, choices=[(1, django_enumfield.enum.Value(b'FOLLOW', 1, 'Follow', athon.enums.FollowStatus)), (2, django_enumfield.enum.Value(b'FOLLOWING', 2, 'Following', athon.enums.FollowStatus))])),
                ('request_status', models.BooleanField(default=False)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('followed_user', models.ForeignKey(related_name='followers', to='athon.AthonUser')),
                ('follower', models.ForeignKey(related_name='following', to='athon.AthonUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='fallowusers',
            name='followed_user',
        ),
        migrations.RemoveField(
            model_name='fallowusers',
            name='follower',
        ),
        migrations.RenameField(
            model_name='athonuser',
            old_name='fallowers_number',
            new_name='followers_number',
        ),
        migrations.RenameField(
            model_name='athonuser',
            old_name='fallowing_number',
            new_name='following_number',
        ),
        migrations.RemoveField(
            model_name='athonuser',
            name='fallow_users',
        ),
        migrations.DeleteModel(
            name='FallowUsers',
        ),
        migrations.AddField(
            model_name='athonuser',
            name='follow_users',
            field=models.ManyToManyField(related_name='related_to_following', through='athon.FollowUsers', to='athon.AthonUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='athonuser',
            name='height',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='athonuser',
            name='weight',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
