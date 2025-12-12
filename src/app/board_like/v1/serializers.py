from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from app.board.models import Board
from app.board_like.models import BoardLike


class BoardLikeToggleSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)

    class Meta:
        model = BoardLike
        fields = [
            "is_liked",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            like, created = BoardLike.objects.get_or_create(
                board_id=self.context["view"].kwargs["board_id"],
                user_id=self.context["request"].user.id,
            )
            if not created:
                like.delete()
                validated_data["is_liked"] = False
                Board.objects.filter(id=self.context["view"].kwargs["board_id"]).update(like_count=F("like_count") - 1)
            else:
                validated_data["is_liked"] = True
                Board.objects.filter(id=self.context["view"].kwargs["board_id"]).update(like_count=F("like_count") + 1)
        return validated_data
