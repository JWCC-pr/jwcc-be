from rest_framework import serializers

from app.pastoral_guidelines.models import PastoralGuidelines


class PastoralGuidelinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastoralGuidelines
        fields = [
            "id",
            "image",
            "category",
            "title",
            "subtitle",
            "body",
            "signature_text",
            "signature_image",
        ]
