from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from api import models
from .models import Project


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('org', 'is_premium')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# class OrganizationAdmin(admin.ModelAdmin):
#     filter_horizontal = ('member',)


class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ('resp', 'member',)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Organization)
admin.site.register(models.Profile)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.PersonalSetting)
admin.site.register(models.Task)
admin.site.register(models.TaskCategory)
admin.site.register(models.AlterResponsible)
admin.site.register(models.JoinApproval)
