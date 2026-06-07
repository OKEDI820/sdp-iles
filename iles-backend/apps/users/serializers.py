from rest_framework import serializers
from .models import User
from apps.common.choices import ROLE_LABELS

class UserSerializer(serializers.ModelSerializer):
    role_label = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name', 
            'role', 'role_label', 'student_number', 'staff_number', 'department', 
            'phone', 'is_active'
        ]
    
    def get_role_label(self, obj):
        return ROLE_LABELS.get(obj.role, obj.role)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'role', 'password', 'student_number', 'staff_number', 'department', 'phone'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user