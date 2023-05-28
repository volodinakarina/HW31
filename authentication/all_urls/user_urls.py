from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import user_views

router = routers.SimpleRouter()
router.register('', user_views.UsersGenericViewSet)

urlpatterns = [
    path('register/', user_views.UserCreateView.as_view(), name='user_register'),
    path('password/change/', user_views.UserChangePasswordView.as_view(), name='user_change_password'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh token'),
]

urlpatterns += router.urls
