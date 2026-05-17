from django.db import migrations


def seed_manage_transaction_permission(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    Role = apps.get_model("permissions", "Role")

    permission, _ = Permission.objects.get_or_create(
        key="view_all_transaction",
        defaults={
            "name": "View All Transaction"
        }
    )

    roles = Role.objects.filter(name__in=["admin", "officer"])

    for role in roles:
        role.permissions.add(permission)


def remove_manage_transaction_permission(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")

    Permission.objects.filter(
        key="view_all_transaction"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("permissions", "0008_assign_user_permissions_to_admin"),
    ]

    operations = [
        migrations.RunPython(
            seed_manage_transaction_permission,
            remove_manage_transaction_permission
        ),
    ]
