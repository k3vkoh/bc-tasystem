from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("courses/", include("courses.urls")),
    path("applications/", include("applications.urls"), name="applications"),
    path("offers/", include("offers.urls"), name="offers"),
]
