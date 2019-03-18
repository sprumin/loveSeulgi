from django.contrib import admin
from django.utils.safestring import mark_safe

from gallery.models import Album, TrashCan


# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "photo", "title", "source", "views", "thumbs", "is_gif", "created_at", )
    ordering = ("-id", "views", "thumbs", )
    list_filter = ("is_gif", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.url, obj.photo.url, obj.photo.width / 3, obj.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


class TrashCanAdmin(admin.ModelAdmin):
    list_display = ("id", "photo_link", )
    ordering = ("-id", )


admin.site.register(Album, AlbumAdmin)
admin.site.register(TrashCan, TrashCanAdmin)
