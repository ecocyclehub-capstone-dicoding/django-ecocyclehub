import uuid
from django.db import models
from django.db.models.functions import Lower

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    price_per_kg = models.IntegerField()
    point_per_kg = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uq_categories_name_ci"
            )
        ]

    def __str__(self):
        return self.name
