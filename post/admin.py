from django.contrib import admin
from django.utils.safestring import mark_safe

from post.models import Notice, Post, Report, NoticeComment, PostComment, ReportComment


# Register your models here.
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "photo", "views", "modified_at", )
    ordering = ("-id", "views", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.url, obj.photo.url, obj.photo.width / 3, obj.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "photo", "views", "thumbs", "modified_at", )
    ordering = ("-id", "views", "thumbs", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.url, obj.photo.url, obj.photo.width / 3, obj.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "photo", "views", "modified_at", )
    ordering = ("-id", "views", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.url, obj.photo.url, obj.photo.width / 3, obj.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'


class NoticeCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "notice", "username", "message", "modified_at", )
    ordering = ("-id", )


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "username", "message", "thumbs", "modified_at", )
    ordering = ("-id", "thumbs", )


class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "username", "message", "modified_at", )
    ordering = ("-id", )


admin.site.register(Notice, NoticeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(NoticeComment, NoticeCommentAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)
