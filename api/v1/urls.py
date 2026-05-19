from django.urls import include, path

urlpatterns = [
    path("users/", include("api.v1.users.urls")),
    path("reports/", include("api.v1.reports.urls")),
    path("chats/", include("api.v1.chats.urls")),
]
