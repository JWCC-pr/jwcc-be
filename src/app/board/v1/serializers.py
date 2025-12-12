from rest_framework import serializers

from app.board.models import Board
from app.board.v1.nested_serializers import UserSerializer


class BoardSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "user",
            "title",
            "body",
            "is_owned",
            "is_liked",
            "hit_count",
            "comment_count",
            "like_count",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
