from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, Task, TaskApplication


# 注册 CustomUser 模型
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role')  # 显示用户名、姓名、角色
    list_filter = ('role',)  # 允许根据角色筛选


# 注册 Task 模型
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'posted_by', 'created_at', 'updated_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')


# 注册 TaskApplication 模型
@admin.register(TaskApplication)
class TaskApplicationAdmin(admin.ModelAdmin):
    list_display = ('task_link', 'applicant', 'status', 'applied_at')  # 使用自定义 task_link
    list_editable = ('status',)
    list_filter = ('status', 'applied_at')

    def task_link(self, obj):
        """
        创建任务链接，点击后跳转到任务的详细页面
        """
        if obj.task:
            return format_html(
                '<a href="/admin/core/task/{}/change/" target="_blank">{}</a>',
                obj.task.id,
                obj.task.title
            )
        return "No Task"

    task_link.short_description = 'Task'  # 修改字段显示名
