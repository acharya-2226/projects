from django.urls import path
from lmsapi.views import TeacherApiView, TeacherListCreateApiView


urlpatterns = [
    path('teacher/<int:pk>/detail/', TeacherApiView.as_view(), name='api.teacher.detail'),
    path('teacher/<int:pk>/update/', TeacherApiView.as_view(), name='api.teacher.update'),
    path('teacher/<int:pk>/edit/', TeacherApiView.as_view(), name='api.teacher.edit'),
    path('teacher/<int:pk>/delete/', TeacherApiView.as_view(), name='api.teacher.delete'),
    path('teacher/create/', TeacherListCreateApiView.as_view(), name='api.teacher.create'),
    path('teacher/list/', TeacherListCreateApiView.as_view(), name='api.teacher.list'),
]