from rest_framework import serializers

from app.contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "office_phone",
            "president_name",
            "president_phone",
        ]
