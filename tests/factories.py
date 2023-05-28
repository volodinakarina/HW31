import datetime

import factory

from ads.models import Category, Ad
from authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    password = "test_password"
    email = factory.Sequence(lambda n: f'person{n}@example.com')
    birth_date = datetime.date(2000, 1, 1)


class ModeratorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    password = "test_password"
    email = factory.Sequence(lambda n: f'person{n}@example.com')
    birth_date = datetime.date(2000, 1, 1)
    role = 'moderator'


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('name')
    slug = 'test1'


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker('name')
    price = factory.Sequence(lambda n: n+1)
    author = factory.SubFactory(UserFactory)
