from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('merchant', '商家'),
        ('influencer', '网红'),
        ('admin', '管理员'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='influencer')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    # 姓名字段
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    # 解决 groups 和 user_permissions 的 related_name 冲突
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # 为 groups 添加 related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # 为 user_permissions 添加 related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # 新增的字段
    image = models.ImageField(upload_to='task_images/', null=True, blank=True)
    file = models.FileField(upload_to='task_files/', null=True, blank=True)

    def __str__(self):
        return self.title

class TaskApplication(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=[('pending', '待审核'), ('approved', '通过'), ('rejected', '拒绝')],default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied for {self.task.title} with status {self.status}"

# 当任务申请被批准后，更新对应任务的状态为 "in_progress"，并拒绝其他申请
@receiver(post_save, sender=TaskApplication)
def update_task_status(sender, instance, **kwargs):
    if instance.status == 'approved':
        task = instance.task
        # 更新任务状态为 in_progress
        task.status = 'in_progress'
        task.save()
        
        # 拒绝该任务的其他未批准的申请
        TaskApplication.objects.filter(
            Q(task=task) & ~Q(id=instance.id)  # 使用 Q 对象组合条件
        ).update(status='rejected')