from django.db import migrations


def assign_view_user_permission_to_officer(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    Role = apps.get_model("permissions", "Role")

    permission = Permission.objects.filter(key="view_user").first()
    if not permission:
        return

    officer = Role.objects.filter(key="officer").first()
    if not officer:
        return

    officer.permissions.add(permission)


def remove_view_user_permission_from_officer(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    Role = apps.get_model("permissions", "Role")

    permission = Permission.objects.filter(key="view_user").first()
    if not permission:
        return

    officer = Role.objects.filter(key="officer").first()
    if not officer:
        return

    officer.permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("permissions", "0010_fix_view_all_transaction_roles"),
    ]

    operations = [
        migrations.RunPython(
            assign_view_user_permission_to_officer,
            remove_view_user_permission_from_officer,
        ),
    ]
