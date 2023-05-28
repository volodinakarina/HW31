from django.urls import path, include
from rest_framework import routers
from selections import views

router_2 = routers.SimpleRouter()
router_2.register('selections', views.SelectionGenericViewSet)

urlpatterns = router_2.urls
