from rest_framework import serializers
from .models import Permission, Role

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["name", "key", "group"]

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Role
        fields = ["id", "name", "key", "permissions"]
