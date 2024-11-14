from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count, Q
from .serializers import CustomUserSerializer, RegisterSerializer, TaskSerializer, TaskApplicationSerializer
from .models import Task, TaskApplication, CustomUser
import logging
from django.shortcuts import redirect


logger = logging.getLogger(__name__)

# 获取自定义用户模型
User = get_user_model()

def redirect_to_login(request):
    return redirect('/api/login/')

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
        user = request.user
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
    permission_classes = [IsAuthenticated]

# 显示单个任务的详情
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

# 自定义权限 - 只有商家才能发布任务
class IsMerchant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'merchant'

# 商家发布任务
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsMerchant]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

# 用户申请任务
class TaskApplicationCreateView(generics.CreateAPIView):
    queryset = TaskApplication.objects.all()
    serializer_class = TaskApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        task_id = self.kwargs.get('pk')
        task = generics.get_object_or_404(Task, id=task_id)
        if task.status != 'available':
            raise ValidationError("This task is not available for application.")
        serializer.save(applicant=self.request.user, task=task)

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = generics.get_object_or_404(Task, id=task_id)
        application_exists = TaskApplication.objects.filter(applicant=request.user, task=task).exists()
        
        if application_exists:
            return Response({"detail": "You have already applied for this task."}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().post(request, *args, **kwargs)

# 用户取消任务申请
class TaskApplicationDeleteView(generics.DestroyAPIView):
    queryset = TaskApplication.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        application_id = kwargs.get('pk')
        try:
            application = TaskApplication.objects.get(id=application_id, applicant=request.user)
            application.delete()
            return Response({"detail": "Application canceled successfully."}, status=status.HTTP_204_NO_CONTENT)
        except TaskApplication.DoesNotExist:
            raise NotFound("Application not found or you don't have permission to delete it.")

# 查看用户已申请的任务
class MyAppliedTasksView(generics.ListAPIView):
    serializer_class = TaskApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskApplication.objects.filter(applicant=self.request.user)

# 查看商家发布的任务
class MyPostedTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(posted_by=self.request.user).annotate(applicants_count=Count('applications'))

# 更新用户信息
class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 更新任务
class UpdateTaskView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Task.objects.filter(posted_by=self.request.user, status__in=['available', 'in_progress'])

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# 商家删除任务
class TaskDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk, posted_by=request.user, status='available')
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or not available"}, status=status.HTTP_404_NOT_FOUND)

# 标记任务为完成
class MarkTaskCompletedView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, posted_by=request.user, status='in_progress')
            task.status = 'completed'
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or not in progress"}, status=status.HTTP_404_NOT_FOUND)
