from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.contact.v1.views import ContactViewSet

router = DefaultRouter()
router.register("contact", ContactViewSet, basename="contact")

urlpatterns = [
    path("", include(router.urls)),
]
