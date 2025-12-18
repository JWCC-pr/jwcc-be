from django.db import transaction
from rest_framework import serializers

from app.liturgy_flower.models import LiturgyFlower
from app.liturgy_flower.v1.nested_serializers import LiturgyFlowerImageSerializer, UserSerializer
from app.liturgy_flower_image.models import LiturgyFlowerImage


class LiturgyFlowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    image_set = LiturgyFlowerImageSerializer(label="이미지", many=True)

    class Meta:
        model = LiturgyFlower
        fields = [
            "id",
            "user",
            "title",
            "comment_count",
            "image_set",
            "created_at",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            image_data_set = validated_data.pop("image_set")
            validated_data["user"] = self.context["request"].user
            liturgy_flower = LiturgyFlower.objects.create(**validated_data)
            LiturgyFlowerImage.objects.bulk_create(
                [
                    LiturgyFlowerImage(
                        liturgy_flower=liturgy_flower,
                        **image_data,
                    )
                    for image_data in image_data_set
                ]
            )
        return liturgy_flower

    def update(self, instance, validated_data):
        with transaction.atomic():
            image_data_set = validated_data.pop("image_set")
            instance = super().update(instance, validated_data)
            instance.image_set.all().delete()
            LiturgyFlowerImage.objects.bulk_create(
                [
                    LiturgyFlowerImage(
                        liturgy_flower=instance,
                        **image_data,
                    )
                    for image_data in image_data_set
                ]
            )
        return instance
