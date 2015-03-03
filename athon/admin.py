from athon import models
from django.contrib.auth.models import User
from django.contrib import admin


admin.site.register(models.Profile)
admin.site.register(models.FollowUsers)
admin.site.register(models.AthleteHistory)
admin.site.register(models.Achievement)
