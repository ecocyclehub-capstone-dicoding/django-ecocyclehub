import uuid
from django.core.validators import MinValueValidator
from django.db import models


class Level(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=100)
    min_points = models.IntegerField(unique=True, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["min_points"]

    def __str__(self):
        return self.name
