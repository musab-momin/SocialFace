from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime 
from django.utils import timezone


User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    dob = models.DateField("date_of_birth")
    gender = models.CharField(max_length=10)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to = 'profile_images')
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_on = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class LikePost(models.Model):
    username = models.CharField(max_length=200)
    post_id = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class FollowingCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following_user_id = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username


class Comment(models.Model):
    commented_by = models.CharField(max_length=200)
    content = models.TextField(blank=False, null=False) 
    number_of_likes = models.IntegerField(default=0)
    publish_date = models.DateTimeField(default=timezone.now)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return  self.content[:10]