from django.db import models

from ads.models import Ad
from authentication.models import User


class Selection(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)
    is_active = models.BooleanField(default=True)

    def __repr__(self):
        return f'Selection({self.name})'

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
