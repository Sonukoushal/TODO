from django.urls import path 
from .views import TaskListCreateView, TaskDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, LogoutAPIView
urlpatterns = [
    path('tasks/',TaskListCreateView.as_view(),name='task-list-create'),
    path('task/<int:pk>/', TaskDetailView.as_view(),name='task_detail'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('register/', RegisterAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]

