from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, RegisterSerializer, TaskSerializer, TaskApplicationSerializer
from .models import Task, TaskApplication
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import BasePermission
from .models import CustomUser
import logging
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

# 获取自定义用户模型
User = get_user_model()

# 用户注册视图
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# 用户信息视图
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # 获取当前登录的用户
        serializer = self.serializer_class(user)
        return Response(serializer.data)

# 用户登出视图（黑名单 Token）
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# 用户登录视图
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

# 显示任务列表
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # 只有登录用户可以查看任务列表

# 显示单个任务的详情
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # 只有登录用户可以查看任务详情

# 只有商家才能发布任务的自定义权限
class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'merchant'

# 商家发布任务
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsMerchant]  # 只有登录用户可以发布任务

    def perform_create(self, serializer):
        logger.info(f"Attempting to create task with data: {serializer.validated_data}")
        serializer.save(posted_by=self.request.user)

class TaskApplicationCreateView(generics.CreateAPIView):
    queryset = TaskApplication.objects.all()
    serializer_class = TaskApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        task_id = self.kwargs.get('pk')
        task = generics.get_object_or_404(Task, id=task_id)
        # 检查任务是否可用
        if task.status != 'available':
            raise ValidationError("This task is not available for application.")

        # Save the task application with the current user as the applicant
        serializer.save(applicant=self.request.user, task=task)

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = generics.get_object_or_404(Task, id=task_id)
        application_exists = TaskApplication.objects.filter(applicant=request.user, task=task).exists()
        
        if application_exists:
            return Response({"detail": "You have already applied for this task."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().post(request, *args, **kwargs)
