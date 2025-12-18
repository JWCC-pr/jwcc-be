from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from app.liturgy_flower.models import LiturgyFlower
from app.liturgy_flower_comment.models import LiturgyFlowerComment
from app.liturgy_flower_comment.v1.nested_serializers import UserSerializer


class LiturgyFlowerCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    parent_id = serializers.IntegerField(label="부모 댓글 ID", write_only=True, allow_null=True)
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)

    class Meta:
        model = LiturgyFlowerComment
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

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["liturgy_flower_id"] = self.context["view"].kwargs["liturgy_flower_id"]
            validated_data["user_id"] = self.context["request"].user.id
            instance = super().create(validated_data)
            LiturgyFlower.objects.filter(id=instance.liturgy_flower_id).update(comment_count=F("comment_count") + 1)
        return instance

    def update(self, instance, validated_data):
        validated_data["is_modified"] = True
        instance = super().update(instance, validated_data)
        return instance
