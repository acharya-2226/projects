from django.contrib import admin
from core.models import Student,Teacher,Assignment,Material

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Assignment)
admin.site.register(Material)
# The above code registers the Student, Teacher, Assignment, and Material models with the Django admin site.
# This allows you to manage these models through the Django admin interface.