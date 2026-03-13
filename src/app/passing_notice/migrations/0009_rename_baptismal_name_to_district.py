from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("passing_notice", "0008_alter_passingnoticecomment_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="passingnotice",
            old_name="baptismal_name",
            new_name="district",
        ),
        migrations.AlterField(
            model_name="passingnotice",
            name="district",
            field=models.CharField(max_length=40, verbose_name="소속 구역"),
        ),
    ]
