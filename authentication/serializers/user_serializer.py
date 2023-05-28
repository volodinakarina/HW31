from rest_framework import serializers

from authentication.models import User, Location
from authentication.serializers.location_serializer import LocationSerializers


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name']
        read_only = ['id']


class UserRetrieveSerializer(serializers.ModelSerializer):
    locations = LocationSerializers(many=True, required=False)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'role', 'password', 'groups', 'is_superuser', 'user_permissions']
        read_only = ['total_ads', 'id']


class UserCreateSerializer(serializers.ModelSerializer):
    locations = LocationSerializers(many=True, required=False)
    password = serializers.CharField(write_only=True)

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations') if 'locations' in self.initial_data else None
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        if self._locations is not None:
            self.validated_data['locations'] = []

            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                self.validated_data['locations'].append(location_obj.id)

        return super().create(validated_data=self.validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', "last_name", 'email', 'locations', 'password', 'birth_date']
        read_only_fields = ['id']


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = LocationSerializers(many=True, required=False)

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations') if 'locations' in self.initial_data else None
        return super().is_valid(raise_exception=raise_exception)

    # def save(self):
    #     user = super().save()
    #
    #     if self._locations is not None:
    #         user.locations.clear()
    #         for location in self._locations:
    #             location_obj, _ = Location.objects.get_or_create(name=location)
    #             user.locations.add(location_obj)
    #
    #     user.save()
    #     return user

    def save(self):
        if self._locations is not None:
            self.validated_data['locations'] = []

            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                self.validated_data['locations'].append(location_obj.id)

        return super().save()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', "last_name", 'email', 'locations', 'birth_date']
        read_only_fields = ['total_ads', 'id']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        old_password = self.validated_data['old_password']
        new_password = self.validated_data['new_password']

        if instance.check_password(old_password):
            instance.set_password(new_password)
        else:
            raise serializers.ValidationError('Wrong password')

        return instance

    # def is_valid(self, raise_exception=False):
    #     is_valid_ = super().is_valid(raise_exception=raise_exception)
    #
    #     if not is_valid_:
    #         return False
    #
    #     old_password = self.initial_data['old_password']
    #     if self.instance.check_password(old_password):
    #         return True
    #     else:
    #         errors = {"error": "You send wrong old password"}
    #
    #     if errors and raise_exception:
    #         raise serializers.ValidationError(errors)
    #
    #     if errors:
    #         return False

    # def save(self, **kwargs):
    #     self.instance.set_password(self.validated_data['new_password'])
    #     self.instance.save()
