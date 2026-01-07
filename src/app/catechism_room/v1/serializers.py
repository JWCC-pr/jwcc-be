from rest_framework import serializers

from app.catechism_room.models import CatechismRoom


class CatechismRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatechismRoom
        fields = [
            "id",
            "name",
            "location",
            "description",
            "created_at",
            "updated_at",
        ]
