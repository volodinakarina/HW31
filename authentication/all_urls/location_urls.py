from django.urls import path, include
from rest_framework import routers

from authentication.views import location_views

router = routers.SimpleRouter()
router.register('', location_views.LocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
