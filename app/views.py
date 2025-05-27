from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User 
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the TODO API!"})


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)
    
    def delete(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields = ['username','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class RegisterAPIView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutAPIView(APIView):
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)





