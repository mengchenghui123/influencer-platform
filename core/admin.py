from django.contrib import admin
from .models import CustomUser, Task, TaskApplication

# 注册模型到管理后台
'''admin.site.register(CustomUser)'''
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # 确保继承自 admin.ModelAdmin
    list_display = ('username', 'first_name', 'last_name', 'role')  # 显示用户名、姓名、角色
    list_filter = ('role',)  # 允许根据角色筛选    



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'posted_by', 'created_at', 'updated_at')
    list_editable = ('status',)  
    list_filter = ('status', 'created_at')

@admin.register(TaskApplication)
class TaskApplicationAdmin(admin.ModelAdmin):
    list_display = ('task', 'applicant', 'status', 'applied_at')
    list_editable = ('status',)  
    list_filter = ('status', 'applied_at')
