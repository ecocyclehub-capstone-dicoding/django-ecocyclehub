import uuid
from django.db import models


class Transaction(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("verified", "Verified"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    handled_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="handled_transactions"
    )

    verified_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_transactions"
    )

    total_price = models.IntegerField(default=0)
    total_weight = models.FloatField(default=0)
    total_points = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id}"

class TransactionDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="details"
    )

    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE
    )

    weight = models.FloatField()

    price_per_kg = models.IntegerField()
    point_per_kg = models.IntegerField()

    total_price = models.IntegerField()
    total_point = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.weight}kg"
