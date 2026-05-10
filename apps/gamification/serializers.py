from rest_framework import serializers

from apps.users.models import User
from .models import Level


class LevelSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        error_messages={
            "required": "The name field is required.",
            "blank": "The name field cannot be empty."
        }
    )

    min_points = serializers.IntegerField(
        error_messages={
            "required": "The minimum points field is required.",
            "invalid": "Minimum points should be a number."
        }
    )

    class Meta:
        model = Level
        fields = "__all__"

    def validate_min_points(self, value):
        queryset = Level.objects.filter(min_points=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Level with this minimum point already exists."
            )

        return value

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email"
        ]

class LevelSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            "id",
            "name",
            "min_points"
        ]

class LeaderboardSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    user = UserSimpleSerializer()
    points = serializers.IntegerField()
    level = LevelSimpleSerializer()
