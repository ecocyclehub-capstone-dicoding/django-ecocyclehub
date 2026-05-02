from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        error_messages={
            "required": "The name field is required.",
            "blank": "The name field cannot be empty."
        }
    )

    price_per_kg = serializers.IntegerField(
        error_messages={
            "required": "The price field is required.",
            "invalid": "Price should a number"
        }
    )

    point_per_kg = serializers.IntegerField(
        error_messages={
            "required": "The point field is required.",
            "invalid": "Point should a number"
        }
    )

    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        queryset = Category.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Category already registered")

        return value
