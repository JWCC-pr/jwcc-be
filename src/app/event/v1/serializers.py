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
            "youtube_link",
            "created_at",
            "updated_at",
        ]
