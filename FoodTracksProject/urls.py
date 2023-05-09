"""
URL configuration for FoodTracksProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from StoreAPI.views import StoreListCreateView, StoreRetrieveUpdateDestroyView
from StoreAPI.address.views import AddressListCreateView, AddressRetrieveUpdateDestroyView
from StoreAPI.openingHours.views import OpeningHoursListCreateView, OpeningHoursRetrieveUpdateDestroyView

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Store API",
      default_version='v1',
      description="Store API for the test Task"
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroyView.as_view(), name='address-retrieve-update-destroy'),
    path('stores/', StoreListCreateView.as_view(), name='store-list-create'),
    path('stores/<int:pk>/', StoreRetrieveUpdateDestroyView.as_view(), name='store-retrieve-update-destroy'),
    path('opening-hours/', OpeningHoursListCreateView.as_view(), name='opening-hours-list-create'),
    path('opening-hours/<int:pk>/', OpeningHoursRetrieveUpdateDestroyView.as_view(), name='opening-hours-retrieve-update-destroy'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]

#