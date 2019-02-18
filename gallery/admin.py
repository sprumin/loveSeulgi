from django.contrib import admin
from django.utils.safestring import mark_safe

from gallery.models import Album


# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "photo", "title", "source", "views", "thumbs", "created_at", )
    ordering = ("-id", )
    list_filter = ("views", "thumbs", )
    readonly_fields = ("photo", "source", "image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.url, obj.photo.url, obj.photo.width / 3, obj.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


admin.site.register(Album, AlbumAdmin)
