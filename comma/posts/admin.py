from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.SavedPost)
admin.site.register(models.CommentLike)