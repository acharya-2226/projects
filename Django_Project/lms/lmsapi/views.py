from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TeacherSerializer
from core.models import Teacher
from rest_framework import serializers

# Create your views here.
# using plain class based views ie apiviews
class TeacherApiView(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Teacher not found")
        
    def get(self, request, pk):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        teacher = self.get_object(pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TeacherListCreateApiView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
       teacher_data = request.data
       serializer = TeacherSerializer(data=teacher_data)
       if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
