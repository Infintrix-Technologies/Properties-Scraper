from django.db import models


class TimeStampMixin:
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class RightMoveProperty(models.Model):
    property_id = models.CharField(max_length=255, db_index=True, unique=True)
    bedrooms = models.IntegerField(default=0, null=True, blank=True)
    bathrooms = models.IntegerField(default=0, null=True, blank=True)
    displayAddress = models.CharField(max_length=255)
    propertySubType = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    propertyUrl = models.URLField()
    image = models.URLField()
    firstVisibleDate = models.DateTimeField()
    propertyTypeFullDescription = models.CharField(max_length=255)
    addedOrReduced = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    branchDisplayName = models.CharField(max_length=255)
    area = models.ForeignKey("Area", null=True, blank=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "rightmove_properties"

    def delete(self):
        self.is_deleted = True
        self.save()


class Note(models.Model):
    text = models.TextField(max_length=255)
    property = models.ForeignKey(
        RightMoveProperty, on_delete=models.CASCADE, related_name="notes"
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notes"


class Area(models.Model):
    name = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name + " | " + self.zip
