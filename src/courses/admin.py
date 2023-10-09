from django.contrib import admin
from .models import Course, ArchivedCourse

# Register your models here.
admin.site.register(Course)
admin.site.register(ArchivedCourse)