from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from .models import User

class RoleFilter(SimpleListFilter):
    title = 'role'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        return (
            ('Student', 'Student'),
            ('College Admin', 'College Admin'),
            ('Coordinator', 'Coordinator'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Student':
            return queryset.filter(student_profile__isnull=False)
        if self.value() == 'College Admin':
            return queryset.filter(collegeadmin_profile__isnull=False)
        if self.value() == 'Coordinator':
            return queryset.filter(coordinator_profile__isnull=False)
        return queryset

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_role', 'get_profile_name', 'get_roll_identifier', 'is_staff')
    list_filter = (RoleFilter, 'is_staff', 'is_superuser', 'is_active')

    def get_role(self, obj):
        if hasattr(obj, 'student_profile'):
            return 'Student'
        elif hasattr(obj, 'collegeadmin_profile'):
            return 'College Admin'
        elif hasattr(obj, 'coordinator_profile'):
            return 'Coordinator'
        return '-'
    get_role.short_description = 'ROLE'
    get_role.admin_order_field = 'role'

    def get_profile_name(self, obj):
        if hasattr(obj, 'student_profile'):
            return obj.student_profile.name
        elif hasattr(obj, 'collegeadmin_profile'):
            return obj.collegeadmin_profile.full_name
        elif hasattr(obj, 'coordinator_profile'):
            return obj.coordinator_profile.full_name
        return '-'
    get_profile_name.short_description = 'PROFILE NAME'

    def get_roll_identifier(self, obj):
        if hasattr(obj, 'student_profile'):
            return str(obj.student_profile.roll)
        elif hasattr(obj, 'collegeadmin_profile'):
            return f"Admin ID: {obj.collegeadmin_profile.id}"
        elif hasattr(obj, 'coordinator_profile'):
            return f"Coord ID: {obj.coordinator_profile.id}"
        return '-'
    get_roll_identifier.short_description = 'ROLL / IDENTIFIER'

from django.contrib.auth.models import User as AuthUser
try:
    admin.site.unregister(AuthUser)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
