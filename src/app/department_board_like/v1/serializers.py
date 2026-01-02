from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from app.department_board.models import DepartmentBoard
from app.department_board_like.models import DepartmentBoardLike


class DepartmentBoardLikeToggleSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)

    class Meta:
        model = DepartmentBoardLike
        fields = [
            "is_liked",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            department_board_id = self.context["view"].kwargs["department_board_id"]
            user_id = self.context["request"].user.id

            like, created = DepartmentBoardLike.objects.get_or_create(
                department_board_id=department_board_id,
                user_id=user_id,
            )
            if not created:
                like.delete()
                validated_data["is_liked"] = False
                DepartmentBoard.objects.filter(id=department_board_id).update(like_count=F("like_count") - 1)
            else:
                validated_data["is_liked"] = True
                DepartmentBoard.objects.filter(id=department_board_id).update(like_count=F("like_count") + 1)
        return validated_data
