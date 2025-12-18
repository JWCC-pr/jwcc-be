from rest_framework import serializers

from app.news.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "thumbnail", "body", "created_at", "updated_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
