from django.forms import ModelForm

from ads.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
