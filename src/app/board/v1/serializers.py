from django.db import transaction
from rest_framework import serializers

from app.board.models import Board
from app.board.v1.nested_serializers import UserSerializer
from app.board_image.models import BoardImage
from app.board_image.v1.nested_serializers import BoardImageSerializer


class BoardSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)
    image_set = BoardImageSerializer(
        label="이미지",
        many=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = Board
        fields = [
            "id",
            "user",
            "title",
            "body",
            "image_set",
            "is_owned",
            "is_liked",
            "hit_count",
            "comment_count",
            "like_count",
            "is_modified",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            image_data_set = validated_data.pop("image_set", [])
            validated_data["user"] = self.context["request"].user

            board = Board.objects.create(**validated_data)

            if image_data_set:
                BoardImage.objects.bulk_create(
                    [
                        BoardImage(
                            board=board,
                            **image_data,
                        )
                        for image_data in image_data_set
                    ]
                )
        return board

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data["is_modified"] = True
            image_data_set = validated_data.pop("image_set", None)

            board = super().update(instance, validated_data)

            if image_data_set is not None:
                board.image_set.all().delete()
                if image_data_set:
                    BoardImage.objects.bulk_create(
                        [
                            BoardImage(
                                board=board,
                                **image_data,
                            )
                            for image_data in image_data_set
                        ]
                    )
        return board
