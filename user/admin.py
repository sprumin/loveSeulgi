from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from user.forms import UserCreationForm
from user.models import User


class UserAdmin(BaseUserAdmin):
    """ User Model Admin"""
    add_form = UserCreationForm

    list_display = ('email', 'username', 'photos_count', 'is_superuser', )
    list_filter = ('is_superuser', )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'is_superuser', 'image_viewer', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ('image_viewer', )

    def photos_count(self, obj):
        return len(obj.photos.all())

    def image_viewer(self, obj):
        photos = ""

        for row in obj.photos.all():
            photos += "<a href='{}'><img src='{}' width='{}' height='{}' /></a>  ".format(
                      row.photo.url, row.photo.url, row.photo.width / 3, row.photo.height / 3)

        return mark_safe(photos)

    image_viewer.short_description = 'Image Viewer'


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
