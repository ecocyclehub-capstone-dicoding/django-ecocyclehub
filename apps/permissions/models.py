import uuid
from django.db import models

class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100, unique=True)
    group = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return str(self.name)
