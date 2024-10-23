from rest_framework import serializers
from .models import CustomUser, Task, TaskApplication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

# 获取自定义用户模型
User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']  # 确保序列化器返回 role

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role', 'phone_number', 'address','first_name','last_name']
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
        first_name=validated_data.get('first_name', ''),
        last_name=validated_data.get('last_name', '')

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
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'phone_number', 'address','first_name','last_name']

class TaskSerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(source='posted_by.username', read_only=True)  # 返回用户名而非ID

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'budget', 'deadline', 'created_at', 'updated_at', 'posted_by','status']
        read_only_fields = ['id', 'created_at', 'updated_at', 'posted_by']
    
    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    
class TaskApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskApplication
        fields = ['id', 'task', 'applicant', 'status', 'applied_at']
        read_only_fields = ['id', 'applicant', 'task', 'status', 'applied_at']


