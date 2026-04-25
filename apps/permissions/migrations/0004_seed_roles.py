from django.db import migrations

ROLES = [
    ("customer", "Customer"),
    ("officer", "Officer"),
    ("admin", "Admin"),
    ("superadmin", "Super Admin"),
]


def create_roles(apps, schema_editor):
    Role = apps.get_model('permissions', 'Role')

    for key, name in ROLES:
        Role.objects.get_or_create(
            key=key,
            defaults={"name": name}
        )


def reverse_roles(apps, schema_editor):
    Role = apps.get_model('permissions', 'Role')

    keys = [r[0] for r in ROLES]
    Role.objects.filter(key__in=keys).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_alter_role_permissions'),
    ]

    operations = [
        migrations.RunPython(create_roles, reverse_roles),
    ]
