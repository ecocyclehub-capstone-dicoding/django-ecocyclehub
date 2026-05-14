from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from apps.permissions.models import Role
from apps.permissions.serializers import RoleSerializer
from .models import User

class UserResponseSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ["id", "name", "email", "role"]

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        error_messages={
            "required": "The name field is required.",
            "blank": "The name field cannot be empty."
        }
    )

    email = serializers.EmailField(
        error_messages={
            "required": "The email field is required.",
            "blank": "The email field cannot be empty."
        }
    )

    password = serializers.CharField(
        write_only=True,
        required=False,
        error_messages={
            "required": "The password field is required.",
            "blank": "The password field cannot be empty."
        }
    )

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(
            key__in=["customer", "officer", "admin"]
        ),
        source="role",
        write_only=True,
        required=True,
        error_messages={
            "required": "The role_id field is required."
        }
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "password",
            "role_id"
        ]
        read_only_fields = ["id"]

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)

        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                "Email already registered"
            )

        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                list(exc.messages)
            ) from exc

        return value

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return User.objects.create_user(
                    email=validated_data["email"],
                    password=validated_data["password"],
                    name=validated_data["name"],
                    role=validated_data["role"],
                )

        except IntegrityError as exc:
            raise serializers.ValidationError(
                {"email": "Email already registered"}
            ) from exc

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        instance.name = validated_data.get(
            "name",
            instance.name
        )

        instance.email = validated_data.get(
            "email",
            instance.email
        )

        instance.role = validated_data.get(
            "role",
            instance.role
        )

        if password:
            validate_password(password)
            instance.set_password(password)

        instance.save()

        return instance
