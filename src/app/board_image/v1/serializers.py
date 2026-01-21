from rest_framework import serializers

from app.board_image.models import BoardImage


class BoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardImage
        fields = [
            "id",
            "image",
        ]
