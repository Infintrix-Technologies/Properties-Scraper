from rest_framework import serializers
from .models import RightMoveProperty, Note, Area


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class RightMovePropertySerializer(serializers.ModelSerializer):
    area_zip = serializers.ReadOnlyField()
    has_notes = serializers.ReadOnlyField()

    notes = NoteSerializer(many=True)

    class Meta:
        model = RightMoveProperty
        exclude = ["area"]
        depth = 1


class AreaSerializer(serializers.ModelSerializer):
    area_zip = serializers.ReadOnlyField()
    text = serializers.ReadOnlyField()
    value = serializers.ReadOnlyField()

    class Meta:
        model = Area
        fields = "__all__"
