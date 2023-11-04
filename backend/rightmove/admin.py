from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models
from django.utils.html import format_html
from rest_framework import viewsets, filters, status
from .models import RightMoveProperty, Note, Area
from .serializers import RightMovePropertySerializer, NoteSerializer, AreaSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F, Value, ExpressionWrapper, BooleanField, Case, When
from django.db.models.functions import Concat
from rest_framework.decorators import action
from rightmove.tasks import scrape_properties

admin.site.site_header = "Alain"
admin.site.register(models.Area)


@admin.action(description="Delete All")
def delete_all(modeladmin, request, queryset):
    queryset.delete()


class NotesInlineAdmin(admin.StackedInline):
    model = models.Note


class RightMovePropertyAdmin(admin.ModelAdmin):
    list_display = [
        "property_id",
        "image_tag",
        "bedrooms",
        "bathrooms",
        "area",
        "show_notes",
        "displayAddress",
        "propertySubType",
        "price",
        "link_url",
        "firstVisibleDate",
        "price",
        "propertyTypeFullDescription",
        "addedOrReduced",
        "phoneNumber",
        "branchDisplayName",
        "is_deleted",
    ]
    actions = [delete_all]
    search_fields = ["property_id", "area__name"]
    list_filter = [
        "is_deleted",
        "area__zip",
        "bedrooms",
        "bathrooms",
    ]
    list_per_page = 10
    inlines = [
        NotesInlineAdmin,
    ]

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        for obj in queryset:
            obj.delete()

    def get_queryset(self, request):
        queryset = (
            models.RightMoveProperty.objects.select_related("area")
            .prefetch_related("notes")
            .annotate(
                area_zip=Concat(
                    F("area__name"), Value(" | "), F("area__zip"), Value("")
                ),
                has_notes=Case(
                    When(notes__isnull=True, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField(),
                ),
            )
            .distinct()
            .order_by("-updatedAt")
        )

        # Check if 'include_deleted' query parameter is present and set to 1
        # include_deleted = self.request.query_params.get("include_deleted")

        # if include_deleted != "1":
        #     # Filter out deleted items
        #     queryset = queryset.filter(is_deleted=False)

        return queryset

    # readonly_fields = ["finn_code", "status", "url"]

    def image_tag(self, obj):
        return format_html(
            f"""\
        <img class="property-image" src="{obj.image}" width="auto" height="100"/>
        """
        )

    def link_url(self, obj):
        return format_html(f'<a href="{obj.propertyUrl}" target="_blank">Link</a>')

    def show_notes(self, obj):
        if obj.has_notes:
            return format_html(
                f'<a property-id={obj.id} class="notes-success notes-btn">Notes</a>'
            )
        else:
            return format_html(
                f'<a property-id={obj.id} class="notes-normal notes-btn">Notes</a>'
            )


admin.site.register(models.RightMoveProperty, RightMovePropertyAdmin)


class NoteAdmin(admin.ModelAdmin):
    list_display = ("text",)
    list_per_page = 20


admin.site.register(models.Note, NoteAdmin)


# from django.contrib import admin

# # Register your models here.
# from django.utils.html import format_html
# from import_export.admin import ImportExportMixin

# from .models import Listing, Price_History


# class PriceHistoryAdmin(admin.TabularInline):
#     model = Price_History


# class ListingAdmin(ImportExportMixin, admin.ModelAdmin):
#     # list_display = ('title','finn_code', 'Model','State',
#     #                 'orignal_price', 'phone_number','link_url' ,'status_tag')
#     list_display = (
#         "title",
#         "Brand",
#         "Model",
#         "orignal_price",
#         "current_price",
#         "Model_Year",
#         "link_url",
#         "status_tag",
#     )
#     search_fields = [
#         "finn_code",
#         "title",
#         "description",
#         "status",
#     ]

#     list_filter = (
#         "status",
#         "Boat_location",
#         "State",
#         "Type",
#         "Brand",
#         "Model_Year",
#         "Engine_Included",
#         "Engine_Type",
#         "Color",
#         "Sleeps",
#         "Seating",
#     )

#     list_per_page = 15

#     readonly_fields = ["finn_code", "status", "url"]

#     inlines = [
#         PriceHistoryAdmin,
#     ]

#     def get_queryset(self, request):
#         return Listing.objects.prefetch_related("history")

#     def current_price(self, obj: Listing):
#         return format_html(obj.current_price_property)

#     def link_url(self, obj):
#         return format_html(
#             f'<a href="{obj.url}" target="_blank"><i class="fas fa-link"></i></a>'
#         )

#     def image_tag(self, obj):
#         return format_html(
#             f"""\
#         <img src="{obj.image}" width="auto" height="100"/>\
#             <div id="myModal" class="modal">

#             <span class="close">&times;</span>

#             <img class="modal-content" id="img01">

#             <div id="caption"></div>
#         </div>
#         """
#         )

#     def status_tag(self, obj):
#         if obj.status:
#             if obj.status == "Active":
#                 status_class = "active"
#             elif obj.status == "Sold":
#                 status_class = "sold"
#             elif obj.status == "SOLGT":
#                 status_class = "sold"
#             elif obj.status == "Expired":
#                 status_class = "expired"
#             elif obj.status == "Inaktiv":
#                 status_class = "inactive"
#             else:
#                 status_class = "None"

#             return format_html(f'<div class="{status_class}" >{obj.status}</div>')
#         else:
#             return format_html(f'<div class="" ></div>')

#     image_tag.short_description = "Image"
#     status_tag.short_description = "Status"


# class PriceHistoryAdmin(admin.ModelAdmin):
#     list_display = (
#         "listing",
#         "changed_price",
#         "price_changed_date",
#         "last_changed_datetime",
#     )
#     list_per_page = 10


# admin.site.register(Listing, ListingAdmin)
# admin.site.register(Price_History, PriceHistoryAdmin)
