from rest_framework import serializers

from app.event.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "thumbnail",
            "title",
            "body",
            "created_at",
            "updated_at",
        ]
