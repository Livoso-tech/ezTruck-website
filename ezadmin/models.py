from django.db import models


class VehicleDetails(models.Model):
    vehicle = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    per_km = models.PositiveIntegerField()
    rate_per_min = models.PositiveIntegerField(null=True)
    vehicle_model = models.CharField(max_length=100, null=True, blank=True)
    waiting_charge = models.CharField(
        max_length=50, default='First 30 min Free')

    def __str__(self):
        return self.vehicle


class VehicleDetails50_100(models.Model):
    vehicle50 = models.CharField(max_length=100)
    vehicle_model50 = models.CharField(max_length=100, null=True, blank=True)
    price50 = models.PositiveIntegerField()
    per_km50 = models.FloatField(max_length=100)

    def __str__(self):
        return self.vehicle50


class VehicleDetailsAbove100(models.Model):
    vehicle100 = models.CharField(max_length=100)
    vehicle_model100 = models.CharField(max_length=100, null=True, blank=True)
    per_km100 = models.FloatField(max_length=100)

    def __str__(self):
        return self.vehicle100


class CustomerDetails(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_number = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=100)
    shop_dealing = models.CharField(max_length=100, null=True, blank=True)


class LocDriverDetails(models.Model):
    locdriver_name = models.CharField(max_length=100)
    locdriver_number = models.CharField(max_length=100)
    locdriver_address = models.CharField(max_length=100)
    locdriver_VechicleNo = models.CharField(max_length=100)
    locdriver_Vechicle_Type = models.CharField(max_length=100)
    locdriver_OCD_OAD = models.CharField(max_length=100)


class LeasVechicleDetails(models.Model):
    owner_name = models.CharField(max_length=100)
    owner_number = models.CharField(max_length=100)
    owner_address = models.CharField(max_length=100)
    owner_vechicleNo = models.CharField(max_length=100)
    owner_vechicle_Type = models.CharField(max_length=100)
    owner_RC_no = models.CharField(max_length=100)
    date_of_aggrement = models.CharField(max_length=100)


class OfflineBookingDetails(models.Model):
    Invoice_No = models.CharField(max_length=100,null=True,blank=True)
    OffBookingDate = models.CharField(max_length=100,null=True,blank=True)
    Customer_Name = models.CharField(max_length=100,null=True,blank=True)
    Customer_Number = models.CharField(max_length=100,null=True,blank=True)
    Customer_Share = models.CharField(max_length=100,null=True,blank=True)
    Driver_Share = models.CharField(max_length=100,null=True,blank=True)
    Payment_Status = models.CharField(max_length=100,null=True,blank=True)
    Date_of_payment = models.CharField(max_length=100,null=True,blank=True)
    Pickup_Location = models.CharField(max_length=100,null=True,blank=True)
    Drop_Location = models.CharField(max_length=100,null=True,blank=True)
    Weightage = models.CharField(max_length=100,null=True,blank=True)
    Km_Booking = models.CharField(max_length=100,null=True,blank=True)
    Booking_Status = models.CharField(max_length=100,null=True,blank=True)
    Driver_Name = models.CharField(max_length=100,null=True,blank=True)
    Driver_Phone = models.CharField(max_length=100,null=True,blank=True)
    Vechicle_Number = models.CharField(max_length=100,null=True,blank=True)
    Vechicle_Type = models.CharField(max_length=100,null=True,blank=True)
    Executive = models.CharField(max_length=100,null=True,blank=True)


class EstimationDetails(models.Model):
    vehicle = models.ForeignKey(VehicleDetails, on_delete=models.DO_NOTHING)
    vehicle_model = models.CharField(max_length=100)
    base_price = models.PositiveIntegerField()
    rate_per_km = models.PositiveIntegerField()
    rate_per_min = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=100)
    customer_no = models.PositiveIntegerField(null=True)
    driver_name = models.CharField(max_length=100)
    driver_no = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.customer_name


class Corporate_Fare_Price(models.Model):
    vehicle_Corporate = models.CharField(max_length=100)
    vehicle_Base_Price = models.FloatField(max_length=100)
    per_km_Corporate = models.FloatField(max_length=100)

    def __str__(self):
        return self.vehicle_Corporate
