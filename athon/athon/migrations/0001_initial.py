# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import athon.enums
import uuid_upload_path.storage
import django_enumfield.enum
import django_enumfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AthonUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', django_enumfield.db.fields.EnumField(default=1, enum=athon.enums.Gender, choices=[
                    (1, django_enumfield.enum.Value(b'MALE', 1, 'Male', athon.enums.Gender)),
                    (2, django_enumfield.enum.Value(b'FEMALE', 2, 'Female', athon.enums.Gender))])),
                ('birthday', models.DateField(null=True, blank=True)),
                ('hometown', models.CharField(max_length=225, null=True, blank=True)),
                ('metric', models.BooleanField(default=False)),
                ('profile_photo',
                 models.ImageField(null=True, upload_to=uuid_upload_path.storage.upload_to, blank=True)),
                ('private_profile', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='athon_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
