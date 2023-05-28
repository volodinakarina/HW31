import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'Location({self.name})'


def user_age_validate(value: datetime.date):
    today = datetime.date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 9:
        raise ValidationError("You must be older than 9 years")


def user_email_validate(value):
    if 'rambler.ru' in value:
        raise ValidationError("email can't be rambler.ru")


class User(AbstractUser):
    ROLES = [
        ('member', 'Участник',),
        ('moderator', 'Модератор'),
        ('admin', "Админ")
    ]

    role = models.CharField(max_length=10, choices=ROLES, default='member')
    age = models.IntegerField(blank=True, null=True)
    locations = models.ManyToManyField("Location")
    birth_date = models.DateField(null=False, validators=[user_age_validate])
    email = models.EmailField(unique=True, validators=[user_email_validate])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        today = datetime.date.today()
        self.age = today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        super().save()

    def __str__(self):
        return f'User({self.username})'
