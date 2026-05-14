from django.db import migrations


def assign_user_permissions(apps, schema_editor):
    Role = apps.get_model(
        "permissions",
        "Role"
    )

    Permission = apps.get_model(
        "permissions",
        "Permission"
    )

    admin = Role.objects.get(key="admin")

    permission_keys = [
        "add_user",
        "view_user",
        "edit_user",
        "delete_user",
    ]

    permissions = Permission.objects.filter(
        key__in=permission_keys
    )

    found = set(
        permissions.values_list(
            "key",
            flat=True
        )
    )

    missing = set(permission_keys) - found

    if missing:
        raise RuntimeError(
            f"Missing permissions: {sorted(missing)}"
        )

    admin.permissions.add(*permissions)


def reverse_assign_user_permissions(apps, schema_editor):
    Role = apps.get_model(
        "permissions",
        "Role"
    )

    Permission = apps.get_model(
        "permissions",
        "Permission"
    )

    admin = Role.objects.get(key="admin")

    permissions = Permission.objects.filter(
        key__in=[
            "add_user",
            "view_user",
            "edit_user",
            "delete_user",
        ]
    )

    admin.permissions.remove(*permissions)


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0007_seed_user_permissions'),
    ]

    operations = [
        migrations.RunPython(
            assign_user_permissions,
            reverse_assign_user_permissions
        ),
    ]
