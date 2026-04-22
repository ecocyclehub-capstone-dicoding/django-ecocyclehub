from rest_framework import serializers
from .models import User
from apps.permissions.serializers import RoleSerializer

class UserResponseSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ["id", "name", "email", "role"]
