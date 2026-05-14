from django.db import migrations

USER_PERMISSIONS = [
    {
        "name": "Add User",
        "key": "add_user",
        "group": "users"
    },
    {
        "name": "View User",
        "key": "view_user",
        "group": "users"
    },
    {
        "name": "Edit User",
        "key": "edit_user",
        "group": "users"
    },
    {
        "name": "Delete User",
        "key": "delete_user",
        "group": "users"
    },
]


def seed_user_permissions(apps, schema_editor):
    Permission = apps.get_model(
        "permissions",
        "Permission"
    )

    for permission in USER_PERMISSIONS:
        Permission.objects.get_or_create(
            key=permission["key"],
            defaults={
                "name": permission["name"],
                "group": permission["group"]
            }
        )


def reverse_user_permissions(apps, schema_editor):
    Permission = apps.get_model(
        "permissions",
        "Permission"
    )

    keys = [
        permission["key"]
        for permission in USER_PERMISSIONS
    ]

    Permission.objects.filter(
        key__in=keys
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0006_assign_permissions_to_roles'),
    ]

    operations = [
        migrations.RunPython(
            seed_user_permissions,
            reverse_user_permissions
        ),
    ]
