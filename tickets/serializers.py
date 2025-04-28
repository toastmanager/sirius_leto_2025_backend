from rest_framework.exceptions import ValidationError
from django.contrib.gis.geos import Point
from rest_framework import serializers

from .models import Ticket, TicketCategory, TicketType
from users.serializers import UserSerializer


class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = "__all__"


class TicketTypeSerializer(serializers.ModelSerializer):
    category = TicketCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketCategory.objects.all(),
        write_only=True,
        required=True,
        source="category",
    )

    class Meta:
        model = TicketType
        fields = ("id", "title", "category", "category_id")
        read_only_fields = ("category_id",)


class TicketSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(
        required=True,
        min_value=-90.0,
        max_value=90.0,
    )
    longitude = serializers.FloatField(
        required=True,
        min_value=-180.0,
        max_value=180.0,
    )

    user = UserSerializer(read_only=True)
    type = TicketTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketType.objects.all(), write_only=True, required=True, source="type"
    )

    class Meta:
        model = Ticket
        fields = (
            "id",
            "latitude",
            "address",
            "longitude",
            "user",
            "title",
            "description",
            "created_at",
            "status",
            "type",
            "type_id",
        )
        read_only_fields = ("user", "status", "created_at", "type")

    def validate(self, data):
        """
        Create the location Point from latitude and longitude.
        """
        lat = data.get("latitude")
        lon = data.get("longitude")

        if lat is not None and lon is not None:
            data["location"] = Point(lon, lat, srid=4326)
            data.pop("latitude", None)
            data.pop("longitude", None)
        elif self.instance is None:
            raise ValidationError(
                "Latitude and Longitude must be provided to create a location."
            )

        return data
