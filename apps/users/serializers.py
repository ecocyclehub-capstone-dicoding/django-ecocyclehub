from rest_framework import serializers
from apps.permissions.serializers import RoleSerializer
from .models import User

class UserResponseSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ["id", "name", "email", "role"]
