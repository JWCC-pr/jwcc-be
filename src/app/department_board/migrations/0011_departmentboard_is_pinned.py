from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("department_board", "0010_alter_departmentboardcomment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="departmentboard",
            name="is_pinned",
            field=models.BooleanField(default=False, verbose_name="고정 여부"),
        ),
    ]
