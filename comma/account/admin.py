from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'jdate_joined')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_type', 'jcreated_at')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserConnection)
admin.site.register(models.FollowRequest)
admin.site.register(models.Activity, ActivityAdmin)