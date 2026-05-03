from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.common.choices import Role

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Read-only-ish view of a user. Used in lists and `me` endpoint."""

    role_label = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "role", "role_label",
            "student_number", "staff_number", "department", "phone",
            "is_active", "date_joined",
        ]
        read_only_fields = ["id", "email", "is_active", "date_joined", "role_label"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Used by admins when creating accounts. Enforces password policy."""

    password = serializers.CharField(write_only=True, required=True, min_length=8)
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "role",
            "student_number", "staff_number", "department", "phone",
            "password",
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        role = attrs.get("role")
        if role == Role.STUDENT and not attrs.get("student_number"):
            raise serializers.ValidationError(
                {"student_number": "Required for student accounts."}
            )
        if role in (Role.WORKPLACE_SUPERVISOR, Role.ACADEMIC_SUPERVISOR, Role.ADMIN):
            if not attrs.get("staff_number"):
                raise serializers.ValidationError(
                    {"staff_number": "Required for staff accounts."}
                )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_new_password(self, value):
        validate_password(value, user=self.context["request"].user)
        return value
