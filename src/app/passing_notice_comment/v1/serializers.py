from rest_framework import serializers

from app.passing_notice_comment.models import PassingNoticeComment
from app.passing_notice_comment.v1.nested_serializers import UserSerializer


class PassingNoticeCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    parent_id = serializers.IntegerField(label="부모 댓글 ID", write_only=True, allow_null=True)
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)

    class Meta:
        model = PassingNoticeComment
        fields = [
            "id",
            "user",
            "parent_id",
            "body",
            "is_owned",
            "is_deleted",
            "created_at",
        ]
        extra_kwargs = {
            "is_deleted": {"read_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        validated_data["passing_notice_id"] = self.context["view"].kwargs["passing_notice_id"]
        validated_data["user_id"] = self.context["request"].user.id
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
