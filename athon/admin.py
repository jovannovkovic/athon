from athon import models

from django.contrib.auth.models import User
from django.contrib import admin


admin.site.register(models.AthonUser)
admin.site.register(models.FollowUsers)