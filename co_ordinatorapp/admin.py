from django.contrib import admin
from co_ordinatorapp.models import Coordinator


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display    = ('full_name', 'email', 'phone', 'department', 'created_at')
    search_fields   = ('first_name', 'last_name', 'email')
    list_filter     = ('department',)
    readonly_fields = ('created_at',)
