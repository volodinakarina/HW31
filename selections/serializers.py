from rest_framework import serializers

from ads.models import Ad
from ads.serializers.ad_serializer import AdSerializer
from authentication.models import User
from authentication.serializers.user_serializer import UserListSerializer
from selections.models import Selection


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']
        read_only = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdSerializer(many=True)
    owner = UserListSerializer()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Selection
        exclude = ['is_active']


class SelectionCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    owner_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Selection
        exclude = ['is_active']


class SelectionUpdateSerializer(serializers.ModelSerializer):
    # items = serializers.PrimaryKeyRelatedField(many=True, queryset=Ad.objects.all())
    owner = UserListSerializer(read_only=True)

    class Meta:
        model = Selection
        fields = ['name', 'items', 'id', 'owner']
        read_only_fields = ['id']
