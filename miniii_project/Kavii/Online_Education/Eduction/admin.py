from django.contrib import admin
from .models import *
admin.site.register(Profile)

class CourseInline(admin.TabularInline):
    model = Course
    extra = 0 

class VideoInline(admin.TabularInline):
    model = Video
    extra = 0

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'total_likes', 'profile_url')
    search_fields = ('name', 'role')
    inlines = [CourseInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher')
    inlines = [VideoInline]


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "number", "created_at")
    search_fields = ("name", "email", "number", "message")
 

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)

