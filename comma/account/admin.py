from django.contrib import admin
from . import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'jdate_joined')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserConnection)
admin.site.register(models.FollowRequest)