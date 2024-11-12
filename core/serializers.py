from rest_framework import serializers
from .models import CustomUser, Task, TaskApplication
from django.contrib.auth import get_user_model

# 获取自定义用户模型
User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    """
    序列化用户模型，提供用户的基本信息，限制 ID、用户名和角色字段只读。
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'address', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器，确保角色选择有效，提供基本用户信息的创建功能。
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role', 'phone_number', 'address', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_role(self, value):
        """确保用户必须选择角色"""
        if not value:
            raise serializers.ValidationError("Role is required.")
        return value

    def create(self, validated_data):
        # 提取传递的数据
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        role = validated_data['role']  # 确保已选择角色
        phone_number = validated_data.get('phone_number', '')  # 默认电话号码为空
        address = validated_data.get('address', '')  # 默认地址为空
        first_name = validated_data.get('first_name', '')  # 去掉逗号
        last_name = validated_data.get('last_name', '')  # 去掉逗号

        # 创建用户并保存角色、电话和地址
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone_number=phone_number,
            address=address,
            first_name=first_name,
            last_name=last_name
        )
        return user
    
class TaskSerializer(serializers.ModelSerializer):
    """
    任务序列化器，提供任务的基本信息，并处理附件字段。只读返回发布者用户名。
    """
    posted_by = serializers.CharField(source='posted_by.username', read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True, allow_empty_file=True)
    applicants_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'budget', 'deadline', 'created_at', 'updated_at', 'posted_by', 'status', 'image', 'file', 'applicants_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'posted_by']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

class TaskApplicationSerializer(serializers.ModelSerializer):
    """
    任务申请序列化器，嵌套显示任务信息，提供只读的任务和申请状态字段。
    """
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskApplication
        fields = ['id', 'task', 'status', 'applied_at']
        read_only_fields = ['id', 'applicant', 'task', 'status', 'applied_at']
