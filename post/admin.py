from django.contrib import admin
from django.utils.safestring import mark_safe

from post.models import Post, Problem, PostComment


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "photo", "views", "thumbs", "modified_at", )
    ordering = ("-id", "views", "thumbs", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.url, obj.photo.url, obj.photo.width / 3, obj.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


class ProblemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "photo", "category", "status", "modified_at", )
    ordering = ("-id", "category", "status", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.photo.url, obj.photo.photo.url, obj.photo.photo.width / 3, obj.photo.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "username", "message", "thumbs", "modified_at", )
    ordering = ("-id", "thumbs", )


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Problem, ProblemAdmin)
