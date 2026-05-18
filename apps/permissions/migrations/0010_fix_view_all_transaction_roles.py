from django.db import migrations


def assign_view_all_transaction_permission(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    Role = apps.get_model("permissions", "Role")

    permission, _ = Permission.objects.update_or_create(
        key="view_all_transaction",
        defaults={
            "name": "View All Transaction",
            "group": "transactions",
        },
    )

    for role in Role.objects.filter(key__in=["admin", "officer"]):
        role.permissions.add(permission)


def remove_view_all_transaction_permission_from_roles(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    Role = apps.get_model("permissions", "Role")

    permission = Permission.objects.filter(key="view_all_transaction").first()

    if not permission:
        return

    for role in Role.objects.filter(key__in=["admin", "officer"]):
        role.permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("permissions", "0009_add_view_all_transaction_permission"),
    ]

    operations = [
        migrations.RunPython(
            assign_view_all_transaction_permission,
            remove_view_all_transaction_permission_from_roles,
        ),
    ]
