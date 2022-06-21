from django.contrib import admin
from socialmedia.models import Profile, Post, LikePost, FollowingCount, Comment


# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowingCount)
admin.site.register(Comment)