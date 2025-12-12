from rest_framework import serializers

from app.liturgy_flower.models import LiturgyFlower


class LiturgyFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiturgyFlower
        fields = [
            "id",
            "title",
            "image",
            "created_at",
        ]
