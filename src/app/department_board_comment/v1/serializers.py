from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from app.department_board.models import DepartmentBoard
from app.department_board_comment.models import DepartmentBoardComment
from app.department_board_comment.v1.nested_serializers import UserSerializer


class DepartmentBoardCommentSerializer(serializers.ModelSerializer):
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)
    user = UserSerializer(label="유저", read_only=True)
    parent_id = serializers.IntegerField(label="부모 댓글 ID", write_only=True, allow_null=True, required=False)

    class Meta:
        model = DepartmentBoardComment
        fields = [
            "id",
            "user",
            "parent_id",
            "body",
            "is_owned",
            "is_modified",
            "is_deleted",
            "created_at",
        ]
        extra_kwargs = {
            "is_deleted": {"read_only": True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["department_board_id"] = self.context["view"].kwargs["department_board_id"]
            validated_data["user_id"] = self.context["request"].user.id
            instance = super().create(validated_data)
            DepartmentBoard.objects.filter(id=instance.department_board_id).update(comment_count=F("comment_count") + 1)
        return instance

    def update(self, instance, validated_data):
        validated_data["is_modified"] = True
        instance = super().update(instance, validated_data)
        return instance
