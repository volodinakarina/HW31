from django.urls import path, include

urlpatterns = [
    path('users/', include('authentication.all_urls.user_urls')),
    path('locations/', include('authentication.all_urls.location_urls')),
]
