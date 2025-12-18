

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_user_last_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="grade",
            field=models.PositiveIntegerField(
                choices=[
                    (1, "총관리자"),
                    (2, "사제 및 수도자"),
                    (3, "사무실"),
                    (4, "단체장"),
                    (5, "명도회"),
                    (6, "본당 신자"),
                    (7, "타본당 신자"),
                ],
                default=7,
                verbose_name="등급",
            ),
        ),
    ]
