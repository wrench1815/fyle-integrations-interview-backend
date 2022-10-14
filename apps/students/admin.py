from django.contrib import admin

from .models import Assignment, Student


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    '''Admin View for Assignment'''

    list_display = [
        'student',
        'teacher',
        'content',
        'grade',
    ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    '''Admin View for Student'''

    list_display = [
        'user',
        'created_at',
    ]
