from django.contrib import admin
from .models import VehicleDetails,VehicleDetails50_100,VehicleDetailsAbove100,\
    Corporate_Fare_Price,OfflineBookingDetails
# Register your models here.
admin.site.register(VehicleDetails)
admin.site.register(VehicleDetails50_100)
admin.site.register(VehicleDetailsAbove100)
admin.site.register(Corporate_Fare_Price)
admin.site.register(OfflineBookingDetails)