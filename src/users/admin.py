from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from courses.models import Course
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'eagleid', 'professor')
    list_filter = ('email', 'first_name', 'last_name', 'eagleid', 'professor')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'eagleid')}),
        ('Permissions', {'fields': ('is_active',
         'is_staff', 'is_superuser', 'professor')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'eagleid')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
