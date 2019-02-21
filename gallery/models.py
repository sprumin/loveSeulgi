from django.db import models


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
    is_gif = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
