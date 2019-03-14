from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from user.forms import UserCreationForm
from user.models import User, UserAlbum


class UserAdmin(BaseUserAdmin):
    """ User Model Admin"""
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_superuser', )
    list_filter = ('is_superuser', )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'is_superuser', )}),
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


class UserAlbumAdmin(admin.ModelAdmin):
    list_display = ("user", "photo", )
    readonly_fields = ("image_viewer", )

    def image_viewer(self, obj):
        return mark_safe(
            "<a href='{}'><img src='{}' width='{}' height='{}' /></a>".format(
                obj.photo.photo.url, obj.photo.photo.url, obj.photo.photo.width / 3, obj.photo.photo.height / 3))

    image_viewer.short_description = 'Image Viewer'

admin.site.register(User, UserAdmin)
admin.site.register(UserAlbum, UserAlbumAdmin)
admin.site.unregister(Group)
