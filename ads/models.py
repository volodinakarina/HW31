from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.db import models
from authentication.models import User


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(unique=True, max_length=10, validators=[MinLengthValidator(5), MaxLengthValidator(10)])

    def __repr__(self):
        return f'Category({self.name})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=50, null=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=1000, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return f'Ads({self.name})'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
