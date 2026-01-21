from rest_framework import serializers

from app.board_image.models import BoardImage


class BoardImageSerializer(serializers.ModelSerializer):
    image = serializers.URLField(label="이미지")

    class Meta:
        model = BoardImage
        fields = ["id", "image"]
        ref_name = "BoardImageNestedSerializer"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["image"] = instance.image.url
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret["image"] = ret["image"].replace(BoardImage._meta.get_field("image").storage.url(""), "")
        return ret
