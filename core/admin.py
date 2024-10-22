from django.contrib import admin
from .models import CustomUser, Task, TaskApplication

# 注册模型到管理后台
admin.site.register(CustomUser)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'budget','created_at', 'updated_at')

@admin.register(TaskApplication)
class TaskApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'task', 'status', 'applied_at')
