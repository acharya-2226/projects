from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView
from core.models import Teacher, Student, Assignment, Material



# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_index.html'
    context_object_name = 'teachers'
    paginate_by = 5

class TeacherCreateView(CreateView):
    model = Teacher
    fields = ['full_name', 'email', 'phone_no', 'department', 'join_date','user']
    template_name = 'teachers/teachers_form.html'
    success_url = 'teachers.index'

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_index.html'