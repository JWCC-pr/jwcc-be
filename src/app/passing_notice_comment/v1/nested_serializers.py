from rest_framework import serializers

from app.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "baptismal_name",
        ]
        ref_name = "PassingNoticeCommentUserSerializer"
