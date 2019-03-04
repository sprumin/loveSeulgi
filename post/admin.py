from django.contrib import admin
from django.utils.safestring import mark_safe

from post.models import Post, Problem


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "photo", "views", "thumbs", "modified_at", )
    ordering = ("-id", "views", "thumbs", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.url, obj.photo.url, obj.photo.width / 3, obj.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


class ProblemAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "photo", "category", "status", "modified_at", )
    ordering = ("-id", "category", "status", )

admin.site.register(Post, PostAdmin)
admin.site.register(Problem, ProblemAdmin)
