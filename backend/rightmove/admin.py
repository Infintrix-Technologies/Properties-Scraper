from django.contrib import admin
from . import models


admin.site.register(models.Note)
admin.site.register(models.Area)


@admin.action(description="Delete All")
def delete_all(modeladmin, request, queryset):
    queryset.delete()


@admin.register(models.RightMoveProperty)
class RightMovePropertyAdmin(admin.ModelAdmin):
    list_display = [
        "property_id",
        "propertyUrl",
        "price",
        "bedrooms",
        "bathrooms",
        "is_deleted",
        "area",
    ]
    actions = [delete_all]
