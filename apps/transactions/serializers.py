from django.db import transaction as db_transaction
from rest_framework import serializers
from apps.categories.models import Category
from apps.users.models import User
from .models import Transaction, TransactionDetail

class TransactionDetailInputSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    weight = serializers.FloatField()

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        return value

class TransactionCreateSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=False)
    items = TransactionDetailInputSerializer(many=True)

    def validate_user_id(self, value):
        try:
            user = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Selected customer does not exist")

        if not user.role or user.role.key != "customer":
            raise serializers.ValidationError("Selected user must be a customer")

        return value

    def validate(self, attrs):
        request_user = self.context["request"].user
        user_id = attrs.get("user_id")

        if request_user.role and request_user.role.key != "customer":
            if not user_id:
                raise serializers.ValidationError({
                    "user_id": "Officer or admin must select a customer user_id"
                })

        if request_user.role and request_user.role.key == "customer" and user_id:
            if str(user_id) != str(request_user.id):
                raise serializers.ValidationError(
                    {"user_id": "Customers can only create transactions for themselves"}
                )

        return attrs

    def create(self, validated_data):
        request_user = self.context["request"].user
        user_id = validated_data.get("user_id")
        items = validated_data["items"]

        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = request_user

        category_ids = [item["category_id"] for item in items]
        categories = Category.objects.in_bulk(category_ids)
        missing_ids = [str(cid) for cid in category_ids if cid not in categories]
        if missing_ids:
            raise serializers.ValidationError(
                {"items": f"Unknown category_id(s): {', '.join(missing_ids)}"}
            )

        with db_transaction.atomic():
            handled_by = (
                request_user
                if request_user.role and request_user.role.key != "customer"
                else None
            )

            transaction = Transaction.objects.create(
                user=user,
                handled_by=handled_by,
                status="pending"
            )
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
