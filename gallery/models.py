from django.db import models

from user.models import User

import datetime


# Create your models here.
class Album(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to="image/seulgi", unique=True)
    name = models.CharField(max_length=24, default="Seulgi")
    title = models.CharField(max_length=64)
    photo_link = models.CharField(max_length=2048)
    source = models.CharField(max_length=2048)
    views = models.IntegerField(default=0)
    thumbs = models.IntegerField(default=0)
    thumbers = models.ManyToManyField(User)
    is_gif = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AlbumComment(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ForeignKey(Album, on_delete=models.CASCADE)
    username = models.CharField(max_length=32)
    message = models.TextField(default="Comment")
    thumbs = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class TrashCan(models.Model):
    id = models.AutoField(primary_key=True)
    photo_link = models.CharField(max_length=2048)

    def __str__(self):
        return self.photo_link
