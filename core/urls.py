from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskCreateView, TaskListView, TaskDetailView, RegisterView, UserDetailView, LogoutView,TaskApplicationCreateView
    
urlpatterns = [
    # API 登录路径
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),  # 使用 /api/login/ 作为 API 登录路径
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户注册、注销等其他API路径
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('api/me/', UserDetailView.as_view(), name='user_detail'),
    
    # API 登录、注册、刷新、注销等用户相关路径
    path('api/tasks/', TaskListView.as_view(), name='api-task-list'),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='api-task-detail'),
    path('api/tasks/create/', TaskCreateView.as_view(), name='api-task-create'),
    # 申请任务 API
    path('api/tasks/<int:pk>/apply/', TaskApplicationCreateView.as_view(), name='api-task-apply'),
]
