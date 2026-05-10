from django.db import migrations

def assign_permissions(apps, schema_editor):
    Role = apps.get_model("permissions", "Role")
    Permission = apps.get_model("permissions", "Permission")

    customer = Role.objects.get(key="customer")
    officer = Role.objects.get(key="officer")
    admin = Role.objects.get(key="admin")
    superadmin = Role.objects.get(key="superadmin")

    # CUSTOMER
    customer_permissions = [
        "create_transaction",
        "view_transaction",
        "view_leaderboard",
        "view_categories",
        "view_customer_dashboard",
    ]

    # OFFICER
    officer_permissions = [
        "view_categories",
        "create_transaction",
        "view_transaction",
        "verify_transaction",
        "view_officer_dashboard",
        "view_leaderboard",
    ]

    # ADMIN
    admin_permissions = [
        "add_categories",
        "view_categories",
        "edit_categories",
        "delete_categories",

        "create_transaction",
        "view_transaction",
        "verify_transaction",

        "view_admin_dashboard",

        "add_level",
        "view_level",
        "edit_level",
        "delete_level",

        "view_leaderboard",
    ]

    # SUPERADMIN
    superadmin_permissions = Permission.objects.all()

    def _resolve_permissions(keys, role_key):
        qs = Permission.objects.filter(key__in=keys)
        found = set(qs.values_list("key", flat=True))
        expected = set(keys)
        missing = expected - found
        if missing:
            raise RuntimeError(
                f"Missing permissions for role '{role_key}': {sorted(missing)}"
            )
        return qs

    customer.permissions.set(_resolve_permissions(customer_permissions, "customer"))
    officer.permissions.set(_resolve_permissions(officer_permissions, "officer"))
    admin.permissions.set(_resolve_permissions(admin_permissions, "admin"))
    superadmin.permissions.set(superadmin_permissions)

def reverse_assign_permissions(apps, schema_editor):
    Role = apps.get_model("permissions", "Role")

    for role in Role.objects.filter(key__in=["customer", "officer", "admin", "superadmin"]):
        role.permissions.clear()

class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0005_seed_permissions'),
    ]

    operations = [
        migrations.RunPython(
            assign_permissions,
            reverse_assign_permissions
        ),
    ]
