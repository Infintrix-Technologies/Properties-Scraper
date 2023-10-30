from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/rightmove/", include("rightmove.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
