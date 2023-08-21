from django.contrib import admin

from .models import Friendship, Post, Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Friendship)
