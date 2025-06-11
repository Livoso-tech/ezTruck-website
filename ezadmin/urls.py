from django.urls import path
from .views import admin_login, admin_logout,admin_index,admin_tables, \
    VehicleCreate,VehicleUpdate,VehicleDelete,VehicleCreate50,VehicleUpdate50, \
    VehicleDelete50,VehicleCreate100,VehicleUpdate100,VehicleDelete100,\
    enterprice_details,driver_details,booking_details,admin_1way_estimator,\
    admin_1way_invoice,admin_customer_details,CustomerCreate,CustomerUpdate,CustomerDelete,\
    admin_loc_driver_details,LocDriverCreate,LocDriverUpdate,LocDriverDelete,\
    admin_lease_vechicle_details,LeaseVechicleCreate,LeaseVechicleUpdate,LeaseVechicleDelete,\
    admin_offline_booking_details,OfflineBookCreate,OfflineBookUpdate,OfflineBookDelete,corporate_fareprice,\
    CorporateCreate,CorporateUpdate,CorporateDelete
urlpatterns = [
    path('admin-login/', admin_login, name='admin-login'),
    path('logout/', admin_logout, name='admin-logout'),
    path('admin-index/', admin_index, name='admin-index'),
    path('admin-tables/', admin_tables, name='admin-tables'),
    path('admin-1way-estimator/', admin_1way_estimator, name='admin-1way-estimator'),
    path('admin-1way-invoice/', admin_1way_invoice, name='admin-1way-invoice'),
    
    #new 
    path('bookings-details/', booking_details, name='admin-booking-details'),
    path('enterprice-details/',enterprice_details,  name='admin-enterprice-details'),
    path('driver-details/', driver_details, name='admin-driver-details'),
    
    #OfflineBookingDetails
    path('admin-off-book-details/', admin_offline_booking_details, name='admin-off-book-details'),
    path('admin-off-book-create/', OfflineBookCreate.as_view(), name='admin-off-book-create'),
    path('admin-off-book-update/<int:pk>/', OfflineBookUpdate.as_view(), name='admin-off-book-update'),
    path('admin-off-book-delete/<int:pk>/', OfflineBookDelete.as_view(), name='admin-off-book-delete'),
    
    #Lease vechicle details
    path('admin-leas-vech-details/', admin_lease_vechicle_details, name='admin-leas-vech-details'),
    path('admin-leas-vech-create/', LeaseVechicleCreate.as_view(), name='admin-leas-vech-create'),
    path('admin-leas-vech-update/<int:pk>/', LeaseVechicleUpdate.as_view(), name='admin-leas-vech-update'),
    path('admin-leas-vech-delete/<int:pk>/', LeaseVechicleDelete.as_view(), name='admin-leas-vech-delete'),
    
    #Local Driver details
    path('admin-loc-driver-details/', admin_loc_driver_details, name='admin-loc-driver-details'),
    path('admin-loc-driver-create/', LocDriverCreate.as_view(), name='admin-loc-driver-create'),
    path('admin-loc-driver-update/<int:pk>/', LocDriverUpdate.as_view(), name='admin-loc-driver-update'),
    path('admin-loc-driver-delete/<int:pk>/', LocDriverDelete.as_view(), name='admin-loc-driver-delete'),
    
    #CustomerDetails
    path('admin-customer_details/', admin_customer_details, name='admin-customer_details'),
    path('customer_create/', CustomerCreate.as_view(), name='admin-customer_create'),
    path('customer_update/<int:pk>/', CustomerUpdate.as_view(), name='admin-customer_update'),
    path('customer_delete/<int:pk>/', CustomerDelete.as_view(), name='admin-customer_delete'),
    
    #0-50
    path('vehicle_create/', VehicleCreate.as_view(), name='admin-vehicle_create'),
    path('vehicle_update/<int:pk>/', VehicleUpdate.as_view(), name='admin-vehicle_update'),
    path('vehicle_delete/<int:pk>/', VehicleDelete.as_view(), name='admin-vehicle_delete'),
    
    #50-100
    path('vehicle_create50/', VehicleCreate50.as_view(), name='admin-veh_create(50-100)'),
    path('vehicle_update50/<int:pk>/', VehicleUpdate50.as_view(), name='admin-veh_update(50-100)'),
    path('vehicle_delete50/<int:pk>/', VehicleDelete50.as_view(), name='admin-veh_delete(50-100)'),
    
    #Above100
    path('vehicle_create100/', VehicleCreate100.as_view(), name='admin-veh_create(100)'),
    path('vehicle_update100/<int:pk>/', VehicleUpdate100.as_view(), name='admin-veh_update(100)'),
    path('vehicle_delete100/<int:pk>/', VehicleDelete100.as_view(), name='admin-veh_delete(100)'),
    
    #corporate fareprice
    path('admin-corporate/', corporate_fareprice, name='admin-corporate'),
    path('admin-corporate_create/', CorporateCreate.as_view(), name='admin-corporate_create'),
    path('admin-corporate_update/<int:pk>/', CorporateUpdate.as_view(), name='admin-corporate_update'),
    path('admin-corporate_delete/<int:pk>/', CorporateDelete.as_view(), name='admin-corporate_delete'),
]