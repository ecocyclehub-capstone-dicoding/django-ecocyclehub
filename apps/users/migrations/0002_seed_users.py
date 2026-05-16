from django.db import migrations
from django.contrib.auth.hashers import make_password


USERS = [
    {
        "name": "Customer",
        "email": "customer@mail.com",
        "role_key": "customer",
    },
    {
        "name": "Officer",
        "email": "officer@mail.com",
        "role_key": "officer",
    },
    {
        "name": "Admin",
        "email": "admin@mail.com",
        "role_key": "admin",
    },
]


def seed_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    Role = apps.get_model("permissions", "Role")

    for item in USERS:
        role = Role.objects.filter(
            key=item["role_key"]
        ).first()

        if not role:
            raise RuntimeError(
                f"Role '{item['role_key']}' not found"
            )

        if User.objects.filter(
            email=item["email"]
        ).exists():
            continue

        User.objects.create(
            name=item["name"],
            email=item["email"],
            password=make_password(None),
            role=role,
        )


def reverse_seed_users(apps, schema_editor):
    # Forward migration is idempotent and may skip pre-existing users.
    # Avoid deleting by email to prevent data loss on rollback.
    return

class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0008_assign_user_permissions_to_admin'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            seed_users,
            migrations.RunPython.noop
        ),
    ]
