from rest_framework import serializers

from app.liturgy_flower_image.models import LiturgyFlowerImage


class LiturgyFlowerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiturgyFlowerImage
        fields = ["id", "image"]
        ref_name = "LiturgyFlowerImageSerializer"
