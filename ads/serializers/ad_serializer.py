from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ads.models import Ad, User, Category


class AdSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True, required=False)
    category_id = serializers.IntegerField(write_only=True, required=False)
    image = serializers.CharField(read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    def is_valid(self, raise_exception=False):
        self._author_id = self.initial_data.pop('author_id') if 'author_id' in self.initial_data else None
        self._category_id = self.initial_data.pop('category_id') if 'category_id' in self.initial_data else None

        is_valid_ = super().is_valid(raise_exception=raise_exception)

        if not is_valid_:
            return False

        try:
            if self._author_id:
                self.validated_data['author'] = User.objects.get(id=self._author_id)
            if self._category_id:
                self.validated_data['category'] = Category.objects.get(id=self._category_id)
        except User.DoesNotExist:
            errors = {"error": "You send wrong author id"}
        except Category.DoesNotExist:
            errors = {"error": "You send wrong category id"}
        else:
            errors = None

        if errors and raise_exception:
            raise ValidationError(errors)

        if errors:
            return False

    def create(self, validated_data):
        if 'is_published' in validated_data:
            del validated_data['is_published']
        if 'author' not in validated_data:
            raise ValidationError("You don't send author id")
        if 'category' not in validated_data:
            raise ValidationError("You don't send category id")

        ad = Ad.objects.create(**validated_data)
        ad.save()
        return ad

    class Meta:
        model = Ad
        fields = "__all__"
