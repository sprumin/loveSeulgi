from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from user.forms import UserCreationForm
from user.models import User


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

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
