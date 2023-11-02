from rest_framework import viewsets, filters, status
from .models import RightMoveProperty, Note, Area
from .serializers import RightMovePropertySerializer, NoteSerializer, AreaSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F, Value, ExpressionWrapper, BooleanField, Case, When
from django.db.models.functions import Concat
from rest_framework.decorators import action
from rightmove.tasks import scrape_properties


class RightMovePropertyViewSet(viewsets.ModelViewSet):
    # queryset = (
    #     RightMoveProperty.objects.filter(is_deleted=False)
    #     .select_related("area")
    #     .prefetch_related("notes")
    #     .order_by("updatedAt")
    # )
    serializer_class = RightMovePropertySerializer
    # pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "displayAddress",
        "propertySubType",
        "propertyTypeFullDescription",
    ]
    ordering_fields = ["property_id", "price", "bedrooms", "bathrooms"]

    def get_queryset(self):
        queryset = (
            RightMoveProperty.objects.select_related("area")
            # .prefetch_related("notes")
            .annotate(
                area_zip=Concat(
                    F("area__name"), Value(" | "), F("area__zip"), Value("")
                ),
                has_notes=Case(
                    When(notes__isnull=True, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField(),
                ),
            ).order_by("updatedAt")
        )

        # Check if 'include_deleted' query parameter is present and set to 1
        include_deleted = self.request.query_params.get("include_deleted")

        if include_deleted != "1":
            # Filter out deleted items
            queryset = queryset.filter(is_deleted=False)

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance: RightMoveProperty = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["GET"])
    def notes(self, request, pk=None):
        queryset = Note.objects.filter(property=pk).order_by("updatedAt")
        print(queryset)
        serializer = NoteSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def list(self, request, *args, **kwargs):
    #     scrape_properties.delay()
    #     return super().list(request, *args, **kwargs)


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.filter().order_by("updatedAt")
    serializer_class = NoteSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = (
        Area.objects.filter()
        .annotate(
            area_zip=Concat(F("name"), Value(" | "), F("zip"), Value("")),
            text=Concat(F("name"), Value(" | "), F("zip"), Value("")),
            value=Concat(F("name"), Value(" | "), F("zip"), Value("")),
        )
        .order_by("updatedAt")
    )
    serializer_class = AreaSerializer
