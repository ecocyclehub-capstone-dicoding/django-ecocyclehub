from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model('permissions', 'Role')

    Role.objects.get_or_create(
        key='customer',
        defaults={'name': 'Customer'}
    )

    Role.objects.get_or_create(
        key='admin',
        defaults={'name': 'Admin'}
    )

    Role.objects.get_or_create(
        key='superadmin',
        defaults={'name': 'Super Admin'}
    )


def reverse_roles(apps, schema_editor):
    Role = apps.get_model('permissions', 'Role')

    Role.objects.filter(key__in=['customer', 'admin', 'superadmin']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_alter_role_permissions'),
    ]

    operations = [
        migrations.RunPython(create_roles, reverse_roles),
    ]
