"""VehicleRentingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
# from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CustomerHome.urls')),
    path('OwnerHome/',include('Owner.urls')),
    path('ManagerHome/',include('Manager.urls')),
    path('RentVehicle/',include('RentVehicle.urls')),
    path('Vehicles/',include('Vehicles.urls')),


    # path('trigger-500/', views.trigger_500_error),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)