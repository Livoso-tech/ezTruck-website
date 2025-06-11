from django.contrib import admin
from .models import drivers_details
from .models import CareerApply
from .models import Bookings
from .models import Enterprice
from .models import ContactUs

# Register your models here.
admin.site.register(drivers_details)
admin.site.register(CareerApply)
admin.site.register(Bookings)
admin.site.register(Enterprice)
admin.site.register(ContactUs)
