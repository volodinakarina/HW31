from django.urls import path, include
from rest_framework import routers

from ads.views.category_views import CategoryViewSet

router = routers.SimpleRouter()
router.register('', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]