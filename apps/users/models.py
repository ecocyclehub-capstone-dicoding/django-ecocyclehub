import uuid
import logging
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from apps.permissions.models import Role

logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        if extra_fields.get("role") is None:
            try:
                extra_fields["role"] = Role.objects.get(key="customer")
            except Role.DoesNotExist as exc:
                raise ValueError(
                    "Default 'customer' role not found. Run data migrations to create default roles before registering users."
                ) from exc
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        if "role" not in extra_fields or extra_fields["role"] is None:
            try:
                extra_fields["role"] = Role.objects.get(key="superadmin")
            except Role.DoesNotExist:
                try:
                    extra_fields["role"] = Role.objects.get(key="admin")
                except Role.DoesNotExist:
                    extra_fields["role"] = None

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None  # using email as the username field
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.ForeignKey('permissions.Role', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()

    def __str__(self):
        return str(self.email)
