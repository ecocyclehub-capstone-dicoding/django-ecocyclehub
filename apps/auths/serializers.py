from django.db import IntegrityError, transaction
from rest_framework import serializers
from apps.users.models import User
from apps.permissions.models import Role

class RegisterSerializer(serializers.ModelSerializer):
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
        error_messages={
            "required": "The password field is required.",
            "blank": "The password field cannot be empty."
        }
    )

    class Meta:
        model = User
        fields = ["name", "email", "password"]
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Minimum 8 characters")
        return value

    def create(self, validated_data):
        role = Role.objects.filter(key="customer").first()
        if role is None:
            raise serializers.ValidationError(
                {"role": "Default customer role is not configured."}
            )

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
