from django.db import migrations


def assign_view_level_permission_to_customer(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    Role = apps.get_model("permissions", "Role")

    permission = Permission.objects.filter(key="view_level").first()
    if not permission:
        return

    customer = Role.objects.filter(key="customer").first()
    if not customer:
        return

    customer.permissions.add(permission)


def remove_view_level_permission_from_customer(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    Role = apps.get_model("permissions", "Role")

    permission = Permission.objects.filter(key="view_level").first()
    if not permission:
        return

    customer = Role.objects.filter(key="customer").first()
    if not customer:
        return

    customer.permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("permissions", "0011_assign_view_user_to_officer"),
    ]

    operations = [
        migrations.RunPython(
            assign_view_level_permission_to_customer,
            remove_view_level_permission_from_customer,
        ),
    ]
