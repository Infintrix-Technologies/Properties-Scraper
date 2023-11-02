from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RightMovePropertyViewSet, NotesViewSet, AreaViewSet


router = DefaultRouter()
router.register(r"properties", RightMovePropertyViewSet, basename="properties")
router.register(r"notes", NotesViewSet, basename="notes")
router.register(r"areas", AreaViewSet, basename="areas")
urlpatterns = []


urlpatterns += router.urls
