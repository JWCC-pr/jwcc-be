from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from app.liturgy_flower.models import LiturgyFlower
from app.liturgy_flower_like.models import LiturgyFlowerLike


class LiturgyFlowerLikeToggleSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)

    class Meta:
        model = LiturgyFlowerLike
        fields = [
            "is_liked",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            like, created = LiturgyFlowerLike.objects.get_or_create(
                liturgy_flower_id=self.context["view"].kwargs["liturgy_flower_id"],
                user_id=self.context["request"].user.id,
            )
            if not created:
                like.delete()
                validated_data["is_liked"] = False
                LiturgyFlower.objects.filter(id=self.context["view"].kwargs["liturgy_flower_id"]).update(
                    like_count=F("like_count") - 1
                )
            else:
                validated_data["is_liked"] = True
                LiturgyFlower.objects.filter(id=self.context["view"].kwargs["liturgy_flower_id"]).update(
                    like_count=F("like_count") + 1
                )
        return validated_data
