from django.db import models

from user.models import User
from gallery.models import Album


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    photo = models.ForeignKey(Album, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024, default="Content")
    comment = models.TextField(max_length=1024, default="Comment")
    views = models.IntegerField(default=0)
    thumbs = models.IntegerField(default=0)


class Problem(models.Model):
    CATEGORY = (
        ("SITE", "Site"),
        ("USER", "User"),
        ("IMAGE", "Image"),
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    photo = models.ForeignKey(Album, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY, default="SITE")
    content = models.TextField(max_length=1024, default="Content")
    status = models.BooleanField(default=False)
