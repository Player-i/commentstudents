from django.contrib import admin
from .models import MyUser, Post, Comment
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Post)
admin.site.register(Comment)