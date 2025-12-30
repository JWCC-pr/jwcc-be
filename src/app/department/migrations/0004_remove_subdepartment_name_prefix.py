import re

from django.db import migrations


def remove_name_prefix(apps, schema_editor):
    SubDepartment = apps.get_model("department", "SubDepartment")
    pattern = re.compile(r"^\d{2}\.\s*")

    for sub in SubDepartment.objects.all():
        new_name = pattern.sub("", sub.name)
        if new_name != sub.name:
            sub.name = new_name
            sub.save(update_fields=["name"])


def restore_name_prefix(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("department", "0003_alter_subdepartment_options_subdepartment_order"),
    ]

    operations = [
        migrations.RunPython(remove_name_prefix, restore_name_prefix),
    ]
