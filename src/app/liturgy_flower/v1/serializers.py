from rest_framework import serializers

from app.liturgy_flower.models import LiturgyFlower
from app.liturgy_flower.v1.nested_serializers import LiturgyFlowerImageSerializer


class LiturgyFlowerSerializer(serializers.ModelSerializer):
    image_set = LiturgyFlowerImageSerializer(label="이미지", many=True)

    class Meta:
        model = LiturgyFlower
        fields = [
            "id",
            "title",
            "image_set",
            "created_at",
        ]
