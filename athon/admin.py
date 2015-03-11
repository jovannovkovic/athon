from athon import models
from django.contrib.auth.models import User
from django.contrib import admin


admin.site.register(models.Profile)
admin.site.register(models.FollowUsers)
admin.site.register(models.AthleteHistory)
admin.site.register(models.Achievement)
admin.site.register(models.Unit)
admin.site.register(models.ExerciseType)
admin.site.register(models.ActivityDetails)
admin.site.register(models.Exercise)
admin.site.register(models.Repetition)
admin.site.register(models.Post)
