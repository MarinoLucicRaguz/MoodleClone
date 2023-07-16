from django.db import migrations


def create_roles(apps, schema_editor):
    Role = apps.get_model('app1', 'Role')
    roles = ['ADMIN', 'STUDENT', 'PROFESSOR']
    Role.objects.bulk_create([Role(name=role) for role in roles])


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),  # Replace with the previous migration file name
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]