from django.urls import include, path

urlpatterns = [
    path("v1/", include("app.user.v1.urls")),
    path("v1/", include("app.presigned_url.v1.urls")),
    path("v1/", include("app.email_verifier.v1.urls")),
]
