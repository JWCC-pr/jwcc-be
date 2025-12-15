from django.contrib import admin

from app.contact.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "office_phone", "president_name", "president_phone"]

    def has_add_permission(self, request):
        if Contact.objects.exists():
            return False
        return super().has_add_permission(request)
