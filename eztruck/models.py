from datetime import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class drivers_details(models.Model):
    """Storing driver details"""
    email = models.EmailField(unique=True)
    driver_name = models.CharField(max_length=80)
    driver_number = models.CharField(max_length=12)
    city = models.CharField(max_length=80,null=True)
    lic_number = models.CharField(max_length=80, unique=True)
    veh_number = models.CharField(max_length=80, unique=True)
    vehicle = models.CharField(max_length=80, null=True)
    booktime = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return str(self.driver_name)
    
#Create Enterprice.
class Enterprice(models.Model):
    """Storing driver details"""
    Enterp_name = models.CharField(max_length=80)
    Enterp_email = models.EmailField(max_length=80)
    Enterp_num = models.CharField(max_length=12)
    Company = models.CharField(max_length=80)
    Enterp_city = models.CharField(max_length=80)
    Enterp_lic_number = models.CharField(max_length=80,null=True)
    Enterp_veh_number = models.CharField(max_length=80,null=True)
    Enterp_vehicle = models.CharField(max_length=80, null=True)
    booktime = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return str(self.Enterp_name)  
      
# CareerApply Model
class CareerApply(models.Model):
    fname     = models.CharField(max_length = 50)
    lname     = models.CharField(max_length = 50)
    dob       = models.DateField(max_length=8)
    gender    = models.CharField( max_length=12)
    app_email = models.EmailField(max_length=128)
    app_phone = models.CharField(max_length=12)
    position  = models.CharField(max_length=128)
    address   = models.CharField(max_length=128)
    location  = models.CharField(max_length=128)
    document  = models.FileField(max_length=128)
    def __str__(self):
        return str(self.app_email)
    
# Bookings Model
class Bookings(models.Model):
    Bname        = models.CharField(max_length = 50)
    Bemail       = models.EmailField(max_length=128)
    Bphone       = models.CharField(max_length=12)
    source       = models.CharField(max_length=128)
    destination  = models.CharField(max_length=128)
    distance     = models.CharField(max_length=128, null=True)
    durations    = models.CharField(max_length=128, null=True)
    total_price  = models.FloatField(max_length=128, null=True)
    truck        = models.CharField(max_length=80, null=True)
    booktime     = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return str(self.Bname)

class ContactUs(models.Model):
    Uname = models.CharField(max_length = 50)
    Umail = models.EmailField(max_length=128)
    Uphn = models.CharField(max_length = 20)
    Usub = models.CharField(max_length = 50)
    Umsg = models.CharField(max_length = 300)
    def __str__(self):
        return str(self.Uname)