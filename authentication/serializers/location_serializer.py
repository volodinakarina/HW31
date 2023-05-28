from rest_framework import serializers

from authentication.models import Location


class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
