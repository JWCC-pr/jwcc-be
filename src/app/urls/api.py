from django.urls import include, path

urlpatterns = [
    path("v1/", include("app.user.v1.urls")),
    path("v1/", include("app.presigned_url.v1.urls")),
    path("v1/", include("app.email_verifier.v1.urls")),
    path("v1/", include("app.notice.v1.urls")),
    path("v1/", include("app.event.v1.urls")),
    path("v1/", include("app.weekly_bulletin.v1.urls")),
    path("v1/", include("app.weekly_bulletin_request.v1.urls")),
    path("v1/", include("app.passing_notice.v1.urls")),
    path("v1/", include("app.passing_notice_comment.v1.urls")),
    path("v1/", include("app.liturgy_flower.v1.urls")),
    path("v1/", include("app.board.v1.urls")),
    path("v1/", include("app.board_comment.v1.urls")),
    path("v1/", include("app.board_like.v1.urls")),
    path("v1/", include("app.document.v1.urls")),
]
