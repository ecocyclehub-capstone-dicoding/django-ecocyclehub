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
        required=True,
        error_messages={
            "required": "The password field is required.",
            "blank": "The password field cannot be empty."
        }
    )

    role_key = serializers.CharField(
        write_only=True,
        required=False,
        error_messages={
            "required": "The role_key field is required.",
            "blank": "The role_key field cannot be empty."
        }
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "password",
            "role_key"
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if self.instance is None:
            if not attrs.get("role_key"):
                raise serializers.ValidationError({
                    "role_key": "The role_key field is required."
                })

        return attrs

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

    def validate_role_key(self, value):
        allowed_roles = ["customer", "officer", "admin"]

        if value not in allowed_roles:
            raise serializers.ValidationError(
                "Invalid role key"
            )

        role = Role.objects.filter(key=value).first()

        if not role:
            raise serializers.ValidationError(
                "Role not found"
            )

        return value

    def create(self, validated_data):
        role_key = validated_data.pop("role_key")

        role = Role.objects.filter(
            key=role_key
        ).first()

        try:
            with transaction.atomic():
                return User.objects.create_user(
                    email=validated_data["email"],
                    password=validated_data["password"],
                    name=validated_data["name"],
                    role=role,
                )

        except IntegrityError as exc:
            raise serializers.ValidationError(
                {"email": "Email already registered"}
            ) from exc

    def update(self, instance, validated_data):
        role_key = validated_data.pop(
            "role_key",
            None
        )

        if role_key:
            role = Role.objects.filter(
                key=role_key
            ).first()

            instance.role = role

        password = validated_data.pop(
            "password",
            None
        )

        instance.name = validated_data.get(
            "name",
            instance.name
        )

        instance.email = validated_data.get(
            "email",
            instance.email
        )

        if password:
            validate_password(password)
            instance.set_password(password)

        instance.save()

        return instance
