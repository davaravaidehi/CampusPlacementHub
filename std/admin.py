from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll', 'name', 'email', 'department', 'course']
    list_filter = ['department', 'course']
    search_fields = ['roll', 'name', 'email']
    readonly_fields = ['roll']  # Optional: prevent editing roll if it's primary key
