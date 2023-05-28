from django.urls import path, include
from rest_framework import routers

from ads.views import ad_views
from ads.views.ad_views import AdGenericViewSet

router = routers.SimpleRouter()
router.register('', AdGenericViewSet)

urlpatterns = [
    path('<int:pk>/image/', ad_views.AdImageUploadView.as_view(), name='ad_image'),
    path('', include(router.urls))
]