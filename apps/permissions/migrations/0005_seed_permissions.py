from django.db import migrations

def seed_permissions(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")

    permissions = [

        # Categories
        {
            "name": "Add Categories",
            "key": "add_categories",
            "group": "categories"
        },
        {
            "name": "View Categories",
            "key": "view_categories",
            "group": "categories"
        },
        {
            "name": "Edit Categories",
            "key": "edit_categories",
            "group": "categories"
        },
        {
            "name": "Delete Categories",
            "key": "delete_categories",
            "group": "categories"
        },

        # Transactions
        {
            "name": "Create Transaction",
            "key": "create_transaction",
            "group": "transactions"
        },
        {
            "name": "Verify Transaction",
            "key": "verify_transaction",
            "group": "transactions"
        },
        {
            "name": "View Transaction",
            "key": "view_transaction",
            "group": "transactions"
        },

        # Dashboard
        {
            "name": "View Customer Dashboard",
            "key": "view_customer_dashboard",
            "group": "dashboard"
        },
        {
            "name": "View Admin Dashboard",
            "key": "view_admin_dashboard",
            "group": "dashboard"
        },
        {
            "name": "View Officer Dashboard",
            "key": "view_officer_dashboard",
            "group": "dashboard"
        },

        # Gamification
        {
            "name": "View Leaderboard",
            "key": "view_leaderboard",
            "group": "gamification"
        },
        {
            "name": "Add Level",
            "key": "add_level",
            "group": "gamification"
        },
        {
            "name": "View Level",
            "key": "view_level",
            "group": "gamification"
        },
        {
            "name": "Edit Level",
            "key": "edit_level",
            "group": "gamification"
        },
        {
            "name": "Delete Level",
            "key": "delete_level",
            "group": "gamification"
        },
    ]

    for permission in permissions:
        Permission.objects.get_or_create(
            key=permission["key"],
            defaults={
                "name": permission["name"],
                "group": permission["group"]
            }
        )


def reverse_permissions(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")

    keys = [
        "add_categories",
        "view_categories",
        "edit_categories",
        "delete_categories",
        "create_transaction",
        "verify_transaction",
        "view_transaction",
        "view_customer_dashboard",
        "view_admin_dashboard",
        "view_officer_dashboard",
        "view_leaderboard",
        "add_level",
        "view_level",
        "edit_level",
        "delete_level"
    ]

    Permission.objects.filter(key__in=keys).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0004_seed_roles'),
    ]

    operations = [
        migrations.RunPython(
            seed_permissions,
            reverse_permissions
        ),
    ]
