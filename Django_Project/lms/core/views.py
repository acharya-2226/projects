from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from core.models import Assignment, Material, Teacher, Student
from django.urls import reverse_lazy

class HomePageView(TemplateView):
    template_name = 'home.html'

class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_index.html'
    context_object_name = 'teachers'
    paginate_by = 5

class TeacherCreateView(CreateView):
    model = Teacher
    fields = ['full_name', 'email', 'department', 'phone_no', 'join_data', 'user']
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('core.teacher.index')

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_index.html'
    context_object_name = 'students'
    paginate_by = 5

class StudentCreateView(CreateView):
    model = Student
    fields = ['full_name', 'email', 'semester', 'phone_no', 'user']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('core.student.index')

class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'

class TeacherUpdateView(UpdateView):
    model = Teacher
    fields = '__all__'
    template_name = 'teachers/teacher_form.html'  # changed for clarity
    success_url = reverse_lazy('core.teacher.index')
    context_object_name = 'teacher'

class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_delete_confirm.html'
    success_url = reverse_lazy('core.teacher.index')
    context_object_name = 'teacher'


class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignments/assignment_index.html'
    context_object_name = 'assignments'
    paginate_by = 5
class AssignmentCreateView(CreateView):
    model = Assignment
    fields = ['title', 'description', 'due_date', 'teacher']
    template_name = 'assignments/assignment_form.html'
    success_url = reverse_lazy('assignment.index')

class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'
class AssignmentUpdateView(UpdateView):
    model = Assignment
    template_name = 'assignments/assignment_update.html'
    fields = '__all__'
    success_url = reverse_lazy('assignment.index')
class AssignmentDeleteView(DeleteView):
    model = Assignment
    context_object_name = 'assignment'
    template_name = 'assignments/assignment_delete_confirm.html'
    success_url = reverse_lazy('assignment.index')
class MaterialListView(ListView):
    model = Material
    template_name = 'materials/materials_index.html'
    context_object_name = 'materials'
    paginate_by = 5
class MaterialCreateView(CreateView):
    model = Material
    fields = ['title', 'description', 'file', 'teacher']
    template_name = 'materials/materials_form.html'
    success_url = reverse_lazy('materials.index')
class MaterialDetailView(DetailView):
    model = Material
    template_name = 'materials/materials_detail.html'
    context_object_name = 'materials'
class MaterialUpdateView(UpdateView):
    model = Material
    template_name = 'materials/materials_update.html'
    fields = '__all__'
    success_url = reverse_lazy('materials.index')
class MaterialDeleteView(DeleteView):
    model = Material
    context_object_name = 'materials'
    template_name = 'materials/materials_delete_confirm.html'
    success_url = reverse_lazy('materials.index')
# Note: The success_url in CreateView, UpdateView, and DeleteView should be a URL pattern name or a URL path.
# If you want to redirect to a specific view after creating, updating, or deleting an object


