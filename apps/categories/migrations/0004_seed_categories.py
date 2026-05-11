from django.db import migrations

CATEGORIES = [
    {
        "name": "Kertas",
        "price_per_kg": 1000,
        "point_per_kg": 150,
    },
    {
        "name": "Plastik PET",
        "price_per_kg": 3500,
        "point_per_kg": 300,
    },
    {
        "name": "Plastik Campur",
        "price_per_kg": 1500,
        "point_per_kg": 180,
    },
    {
        "name": "Kaleng Aluminium",
        "price_per_kg": 12000,
        "point_per_kg": 500,
    },
    {
        "name": "Besi",
        "price_per_kg": 4000,
        "point_per_kg": 250,
    },
    {
        "name": "Kaca",
        "price_per_kg": 500,
        "point_per_kg": 100,
    },
    {
        "name": "Elektronik",
        "price_per_kg": 8000,
        "point_per_kg": 450,
    },
    {
        "name": "Minyak Jelantah",
        "price_per_kg": 6000,
        "point_per_kg": 350,
    },
    {
        "name": "Organik",
        "price_per_kg": 300,
        "point_per_kg": 80,
    },
    {
        "name": "Tekstil",
        "price_per_kg": 2000,
        "point_per_kg": 200,
    },
]

def seed_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')


    for category in CATEGORIES:
        Category.objects.get_or_create(
            name=category["name"],
            defaults=category
        )

def reverse_categories(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    names = [cat["name"] for cat in CATEGORIES]
    Category.objects.filter(name__in=names).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_category_point_per_kg_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_categories),
    ]
