from django.db import transaction as db_transaction
from rest_framework import serializers
from apps.categories.models import Category
from .models import Transaction, TransactionDetail

class TransactionDetailInputSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    weight = serializers.FloatField()

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        return value

class TransactionCreateSerializer(serializers.Serializer):
    items = TransactionDetailInputSerializer(many=True)

    def create(self, validated_data):
        user = self.context["request"].user
        items = validated_data["items"]

        category_ids = [item["category_id"] for item in items]
        categories = Category.objects.in_bulk(category_ids)
        missing_ids = [str(cid) for cid in category_ids if cid not in categories]
        if missing_ids:
            raise serializers.ValidationError(
                {"items": f"Unknown category_id(s): {', '.join(missing_ids)}"}
            )

        with db_transaction.atomic():
            transaction = Transaction.objects.create(user=user, status="pending")
            total_price = 0
            total_points = 0
            total_weight = 0

            for item in items:
                category = categories[item["category_id"]]

                weight = item["weight"]

                price_per_kg = category.price_per_kg
                point_per_kg = category.point_per_kg

                item_total_price = weight * price_per_kg
                item_total_point = weight * point_per_kg

                TransactionDetail.objects.create(
                    transaction=transaction,
                    category=category,
                    weight=weight,
                    price_per_kg=price_per_kg,
                    point_per_kg=point_per_kg,
                    total_price=item_total_price,
                    total_point=item_total_point
                )

                total_price += item_total_price
                total_points += item_total_point
                total_weight += weight

            transaction.total_price = total_price
            transaction.total_points = total_points
            transaction.total_weight = total_weight
            transaction.save(update_fields=["total_price", "total_points", "total_weight"])

        return transaction

class TransactionSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "total_price",
            "total_points",
            "total_weight",
            "status",
            "created_at",
            "details"
        ]

    def get_details(self, obj):
        return [
            {
                "category": d.category.name,
                "weight": d.weight,
                "total_price": d.total_price,
                "total_point": d.total_point
            }
            for d in obj.details.all()
        ]

class AdminTransactionSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    handled_by = serializers.SerializerMethodField()
    verified_by = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "handled_by",
            "verified_by",
            "total_price",
            "total_points",
            "total_weight",
            "status",
            "created_at",
            "verified_at",
            "details"
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.name,
        }

    def get_handled_by(self, obj):
        if not obj.handled_by:
            return None

        return {
            "id": obj.handled_by.id,
            "name": obj.handled_by.name,
        }

    def get_verified_by(self, obj):
        if not obj.verified_by:
            return None

        return {
            "id": obj.verified_by.id,
            "name": obj.verified_by.name,
        }

    def get_details(self, obj):
        return [
            {
                "category": d.category.name,
                "weight": d.weight,
                "price_per_kg": d.price_per_kg,
                "point_per_kg": d.point_per_kg,
                "total_price": d.total_price,
                "total_point": d.total_point
            }
            for d in obj.details.all()
        ]
