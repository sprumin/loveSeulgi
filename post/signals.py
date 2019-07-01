from django.db.models.signals import pre_save
from django.dispatch import receiver

from post.models import Post, Report

import magic


@receiver(pre_save, sender=Post)
def post_image_check(sender, instance, *args, **kwargs):
    if instance.photo:
        mime_type = magic.from_buffer(instance.photo.read(1024), mime=True)

        if not mime_type.split("/")[0] == "image":
            raise ValueError("Invalid Image")


@receiver(pre_save, sender=Report)
def report_image_check(sender, instance, *args, **kwargs):
    if instance.photo:
        mime_type = magic.from_buffer(instance.photo.read(1024), mime=True)

        if not mime_type.split("/")[0] == "image":
            raise ValueError("Invalid Image")
