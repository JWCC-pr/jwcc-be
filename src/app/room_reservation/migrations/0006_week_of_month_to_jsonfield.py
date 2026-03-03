from django.db import migrations, models


def convert_week_of_month_to_list(apps, schema_editor):
    """기존 smallint week_of_month 값을 jsonb 리스트로 변환."""
    RepeatRoomReservation = apps.get_model("room_reservation", "RepeatRoomReservation")
    for obj in RepeatRoomReservation.objects.all():
        old_val = obj.week_of_month
        if old_val is not None:
            obj.week_of_month = [old_val]
        else:
            obj.week_of_month = []
        obj.save(update_fields=["week_of_month"])


def convert_week_of_month_to_int(apps, schema_editor):
    """롤백: jsonb 리스트를 다시 smallint로 변환."""
    RepeatRoomReservation = apps.get_model("room_reservation", "RepeatRoomReservation")
    for obj in RepeatRoomReservation.objects.all():
        val = obj.week_of_month
        if isinstance(val, list) and val:
            obj.week_of_month = val[0]
        else:
            obj.week_of_month = None
        obj.save(update_fields=["week_of_month"])


class Migration(migrations.Migration):

    dependencies = [
        ("room_reservation", "0005_repeatroomreservation_organization_name_and_more"),
    ]

    operations = [
        # 0) CHECK 제약조건 제거
        migrations.RunSQL(
            sql="ALTER TABLE repeat_room_reservation DROP CONSTRAINT IF EXISTS repeat_room_reservation_week_of_month_check;",
            reverse_sql="ALTER TABLE repeat_room_reservation ADD CONSTRAINT repeat_room_reservation_week_of_month_check CHECK (week_of_month >= 0);",
        ),
        # 1) smallint → text (중간 단계)
        migrations.RunSQL(
            sql="ALTER TABLE repeat_room_reservation ALTER COLUMN week_of_month TYPE text USING week_of_month::text;",
            reverse_sql="ALTER TABLE repeat_room_reservation ALTER COLUMN week_of_month TYPE smallint USING week_of_month::smallint;",
        ),
        # 2) text → jsonb
        migrations.RunSQL(
            sql="ALTER TABLE repeat_room_reservation ALTER COLUMN week_of_month TYPE jsonb USING CASE WHEN week_of_month IS NOT NULL THEN jsonb_build_array(week_of_month::int) ELSE '[]'::jsonb END;",
            reverse_sql="ALTER TABLE repeat_room_reservation ALTER COLUMN week_of_month TYPE text USING (week_of_month->>0);",
        ),
        # 3) NULL → []
        migrations.RunSQL(
            sql="UPDATE repeat_room_reservation SET week_of_month = '[]'::jsonb WHERE week_of_month IS NULL;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        # 4) Django 모델 상태 동기화
        migrations.AlterField(
            model_name="repeatroomreservation",
            name="week_of_month",
            field=models.JSONField(blank=True, default=list, verbose_name="반복 주차"),
        ),
    ]
