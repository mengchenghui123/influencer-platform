from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    home,TaskCreateView, TaskListView, TaskDetailView, RegisterView, UserDetailView, LogoutView,
    TaskApplicationCreateView, MyAppliedTasksView, MyPostedTasksView, TaskApplicationDeleteView,
    UpdateUserProfileView, UpdateTaskView, TaskDeleteView, MarkTaskCompletedView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),

    # 用户认证相关 API
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),  # 登录路径
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 Token

    # 用户注册、个人信息和注销
    path('api/register/', RegisterView.as_view(), name='api-register'),  # 注册
    path('api/logout/', LogoutView.as_view(), name='api-logout'),  # 注销
    path('api/me/', UserDetailView.as_view(), name='user_detail'),  # 查看用户信息
    path('api/update-profile/', UpdateUserProfileView.as_view(), name='update-profile'),  # 更新用户信息

    # 任务相关 API
    path('api/tasks/', TaskListView.as_view(), name='api-task-list'),  # 查看所有任务
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='api-task-detail'),  # 查看单个任务详情
    path('api/tasks/create/', TaskCreateView.as_view(), name='api-task-create'),  # 创建任务
    path('api/tasks/<int:pk>/update/', UpdateTaskView.as_view(), name='update-task'),  # 更新任务
    path('api/tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),  # 删除任务
    path('api/tasks/<int:pk>/mark_completed/', MarkTaskCompletedView.as_view(), name='mark_task_completed'),  # 标记任务为完成

    # 任务申请相关 API
    path('api/tasks/<int:pk>/apply/', TaskApplicationCreateView.as_view(), name='api-task-apply'),  # 申请任务
    path('api/my-applied-tasks/', MyAppliedTasksView.as_view(), name='my-applied-tasks'),  # 查看已申请任务
    path('api/my-posted-tasks/', MyPostedTasksView.as_view(), name='my-posted-tasks'),  # 查看已发布任务
    path('api/task-applications/<int:pk>/', TaskApplicationDeleteView.as_view(), name='task-application-delete'),  # 取消任务申请
]

# 仅在开发环境启用媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
