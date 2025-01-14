from django.urls import path
from . import views
from django.conf.urls import include


urlpatterns = [
    path('UploadVehicle/', views.upload_vehicle,name="UploadVehicle"),
    path('Owner/',include("Owner.urls")),
    path('Manager/',include("Manager.urls"))
]
