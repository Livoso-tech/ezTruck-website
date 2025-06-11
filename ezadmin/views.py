from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VehicleDetails, VehicleDetails50_100, VehicleDetailsAbove100,\
    CustomerDetails, LocDriverDetails, LeasVechicleDetails,\
    OfflineBookingDetails,Corporate_Fare_Price
from eztruck.models import Bookings, drivers_details, Enterprice, CareerApply, ContactUs
from django.views.generic import DeleteView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
import googlemaps
import re
# Create your views here.


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin-index')
        else:
            # print('Username Or Password is incorrect')
            messages.error(request, 'Username Or Password is incorrect')
    return render(request, 'admin-login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin-login')


@login_required(login_url='admin_login')
def admin_index(request):
    # eztruck databases
    driverdetails = drivers_details.objects.count()
    enterpricedetails = Enterprice.objects.count()
    Careerapply = CareerApply.objects.count()
    Booking = Bookings.objects.count()
    Contactus = ContactUs.objects.count()
    data = {'driverdetails': driverdetails, 'enterpricedetails': enterpricedetails,
            'Careerapply': Careerapply, 'Booking': Booking, 'Contactus': Contactus}
    return render(request, 'admin-index.html', data)


@login_required(login_url='admin_login')
# for admin_offline_booking_details
def admin_offline_booking_details(request):
    offbookdetails = OfflineBookingDetails.objects.all()
    context = {'offbookdetails': offbookdetails}
    return render(request, 'admin-off-book-details.html', context)


class OfflineBookCreate(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    model = OfflineBookingDetails
    fields = '__all__'
    success_url = '/admin-off-book-details/'
    template_name = 'admin-off-book-create.html'


class OfflineBookUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = OfflineBookingDetails
    success_url = '/admin-off-book-details/'
    fields = '__all__'
    template_name = 'admin-off-book-update.html'


class OfflineBookDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = OfflineBookingDetails
    success_url = '/admin-off-book-details/'
    template_name = 'admin-off-book-delete.html'


@login_required(login_url='admin_login')
# for admin_lease_vechicle_details
def admin_lease_vechicle_details(request):
    leasvechicledetails = LeasVechicleDetails.objects.all()
    context = {'leasvechicle': leasvechicledetails}
    return render(request, 'admin-leas-vech-details.html', context)


class LeaseVechicleCreate(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    model = LeasVechicleDetails
    fields = '__all__'
    success_url = '/admin-leas-vech-details/'
    template_name = 'admin-leas-vech-create.html'


class LeaseVechicleUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = LeasVechicleDetails
    success_url = '/admin-leas-vech-details/'
    fields = '__all__'
    template_name = 'admin-leas-vech-update.html'


class LeaseVechicleDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = LeasVechicleDetails
    success_url = '/admin-leas-vech-details/'
    template_name = 'admin-leas-vech-delete.html'


@login_required(login_url='admin_login')
# for admin_customer_details
def admin_loc_driver_details(request):
    locdriverdetails = LocDriverDetails.objects.all()
    context = {'locdriver': locdriverdetails}
    return render(request, 'admin-loc-driver-details.html', context)


class LocDriverCreate(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    model = LocDriverDetails
    fields = '__all__'
    success_url = '/admin-loc-driver-details/'
    template_name = 'admin-loc-driver-create.html'


class LocDriverUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = LocDriverDetails
    success_url = '/admin-loc-driver-details/'
    fields = '__all__'
    template_name = 'admin-loc-driver-update.html'


class LocDriverDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = LocDriverDetails
    success_url = '/admin-loc-driver-details/'
    template_name = 'admin-loc-driver-delete.html'


@login_required(login_url='admin_login')
# for admin_customer_details
def admin_customer_details(request):
    customerdetails = CustomerDetails.objects.all()
    context = {'customer': customerdetails}
    return render(request, 'admin-customer_details.html', context)


class CustomerCreate(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    model = CustomerDetails
    fields = '__all__'
    success_url = '/admin-customer_details/'
    template_name = 'admin-customer_create.html'


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = CustomerDetails
    success_url = '/admin-customer_details/'
    fields = '__all__'
    template_name = 'admin-customer_update.html'


class CustomerDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = CustomerDetails
    success_url = '/admin-customer_details/'
    template_name = 'admin-customer_delete.html'


@login_required(login_url='admin_login')
def admin_1way_estimator(request):
    if request.method == 'POST':
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['VechicleType']

        # ---Map API--
        gmaps = googlemaps.Client(
            key='AIzaSyCqM7uF9c0ZMQjdssHqSMJJ3mBcmz5RNS0')
        my_dist = gmaps.distance_matrix(sour, dest)['rows'][0]['elements'][0]

        database_dist = my_dist['distance']['text']
        database_time = my_dist['duration']['text']

        km = my_dist['distance']['text'].split(" ")[0]
        total_dist1 = re.sub(',', "", km)
        total_time1 = my_dist['duration']['value']

        conv_dist1 = float(total_dist1)
        minutes = total_time1 // 60
        # for 0 - 30
        bp = [i.price for i in VehicleDetails.objects.all()]
        perkm = [i.per_km for i in VehicleDetails.objects.all()]
        permin = [i.rate_per_min for i in VehicleDetails.objects.all()]
        waiting = [i.waiting_charge for i in VehicleDetails.objects.all()]
        v = [i.vehicle for i in VehicleDetails.objects.all()]

        # for 30-99
        bp99 = [i.price50 for i in VehicleDetails50_100.objects.all()]
        perkm99 = [i.per_km50 for i in VehicleDetails50_100.objects.all()]
        v99 = [i.vehicle50 for i in VehicleDetails50_100.objects.all()]

        # for above 100
        perkm100 = [i.per_km100 for i in VehicleDetailsAbove100.objects.all()]
        v100 = [i.vehicle100 for i in VehicleDetailsAbove100.objects.all()]

        # for 0 - 30
        if bvehicle == v[0]:
            base_fare = bp[0]
            per_km = perkm[0]
            per_min = permin[0]
            wait_chrg = int(waiting[0])
        elif bvehicle == v[1]:
            base_fare = bp[1]
            per_km = perkm[1]
            per_min = permin[1]
            wait_chrg = int(waiting[1])
        elif bvehicle == v[2]:
            base_fare = bp[2]
            per_km = perkm[2]
            per_min = permin[2]
            wait_chrg = int(waiting[2])
        elif bvehicle == v[3]:
            base_fare = bp[3]
            per_km = perkm[3]
            per_min = permin[3]
            wait_chrg = int(waiting[3])

        # for 30-99
        if bvehicle == v99[0]:
            base_fare99 = bp99[0]
            per_km99 = perkm99[0]
        elif bvehicle == v99[1]:
            base_fare99 = bp99[1]
            per_km99 = perkm99[1]
        elif bvehicle == v99[2]:
            base_fare99 = bp99[2]
            per_km99 = perkm99[2]
        elif bvehicle == v99[3]:
            base_fare99 = bp99[3]
            per_km99 = perkm99[3]

        # for above 100
        if bvehicle == v100[0]:
            per_km100 = perkm100[0]
        elif bvehicle == v100[1]:
            per_km100 = perkm100[1]
        elif bvehicle == v100[2]:
            per_km100 = perkm100[2]
        elif bvehicle == v100[3]:
            per_km100 = perkm100[3]

        # for 0 - 30
        if (conv_dist1 > 2.5 and conv_dist1 <= 30):
            if bvehicle.lower() == 'auto' and minutes > wait_chrg:
                driver_fare = ((conv_dist1 * per_km) +
                               ((minutes - wait_chrg) * per_min) + base_fare)

            elif bvehicle.lower() == 'tata ace' and minutes > wait_chrg:
                driver_fare = ((conv_dist1 * per_km) +
                               ((minutes - wait_chrg) * per_min) + base_fare)

            elif bvehicle.lower() == 'small pickup' and minutes > wait_chrg:
                driver_fare = ((conv_dist1 * per_km) +
                               ((minutes - wait_chrg) * per_min) + base_fare)

            elif bvehicle.lower() == 'large pickup' and minutes > wait_chrg:
                driver_fare = ((conv_dist1 * per_km) +
                               ((minutes - wait_chrg) * per_min) + base_fare)

            else:
                driver_fare = ((conv_dist1 * per_km) + base_fare)

        # for 30-99
        if (conv_dist1 > 30 and conv_dist1 <= 99):
            if bvehicle.lower() == 'auto':
                driver_fare = (2 * conv_dist1 * per_km99) + base_fare99

            elif bvehicle.lower() == 'tata ace':
                driver_fare = (2 * conv_dist1 * per_km99) + base_fare99

            elif bvehicle.lower() == 'small pickup':
                driver_fare = (2 * conv_dist1 * per_km99) + base_fare99

            elif bvehicle.lower() == 'large pickup':
                driver_fare = (2 * conv_dist1 * per_km99) + base_fare99

            else:
                driver_fare = (2 * conv_dist1 * per_km99) + base_fare99

        # for above 100
        if (conv_dist1 > 99):
            if bvehicle.lower() == 'auto':
                driver_fare = (2 * conv_dist1 * per_km100)

            elif bvehicle.lower() == 'tata ace':
                driver_fare = (2 * conv_dist1 * per_km100)

            elif bvehicle.lower() == 'small pickup':
                driver_fare = (2 * conv_dist1 * per_km100)

            elif bvehicle.lower() == 'large pickup':
                driver_fare = (2 * conv_dist1 * per_km100)

        commission = driver_fare * (5 / 100)
        float_value = driver_fare + commission
        estimate = "{:.2f}".format(float_value)

        context = {
            'to': sour,
            'from': dest,
            'VechicleType': bvehicle,
            'distance': database_dist,
            'duration': database_time,
            'TotalCost': estimate,
        }
        return render(request, 'admin-1way-invoice.html', context)
    return render(request, 'admin-1way-estimator.html')


@login_required(login_url='admin_login')
def admin_1way_invoice(request):
    return render(request, 'admin-1way-invoice.html')


@login_required(login_url='admin_login')
def admin_tables(request):
    data = VehicleDetails.objects.all()
    data50 = VehicleDetails50_100.objects.all()
    data100 = VehicleDetailsAbove100.objects.all()
    context = {'data': data, 'data50': data50, 'data100': data100}
    return render(request, 'admin-tables.html', context)


@login_required(login_url='admin_login')
def booking_details(request):
    data = Bookings.objects.all()
    context = {'data': data}
    return render(request, 'admin-booking-details.html', context)


@login_required(login_url='admin_login')
def driver_details(request):
    data1 = drivers_details.objects.all()
    context = {'data1': data1}
    return render(request, 'admin-driver-details.html', context)


@login_required(login_url='admin_login')
def enterprice_details(request):
    data2 = Enterprice.objects.all()
    context = {'data2': data2}
    return render(request, 'admin-enterprice-details.html', context)


# Enterprice delete booking
class EnterpriseDelete(LoginRequiredMixin, DeleteView):
    model = Enterprice
    success_url = '/admin-offline-booking/'
    template_name = 'admin-enterprise-delete.html'

# driver delete booking


class DriverDelete(LoginRequiredMixin, DeleteView):
    model = drivers_details
    success_url = '/admin-offline-booking/'
    template_name = 'admin-driver-delete.html'

# for fare price 0-50


class VehicleCreate(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    model = VehicleDetails
    fields = '__all__'
    success_url = '/admin-tables/'
    template_name = 'admin-vehicle_create.html'


class VehicleUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = VehicleDetails
    success_url = '/admin-tables/'
    fields = '__all__'
    template_name = 'admin-vehicle_update.html'


class VehicleDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = VehicleDetails
    success_url = '/admin-tables/'
    template_name = 'admin-vehicle_delete.html'

# for fare price 50-100


class VehicleCreate50(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    success_url = '/admin-tables/'
    model = VehicleDetails50_100
    fields = '__all__'
    template_name = 'admin-veh_create(50-100).html'


class VehicleUpdate50(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = VehicleDetails50_100
    success_url = '/admin-tables/'
    fields = '__all__'
    template_name = 'admin-veh_update(50-100).html'


class VehicleDelete50(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = VehicleDetails50_100
    success_url = '/admin-tables/'
    template_name = 'admin-veh_delete(50-100).html'

# for fare price above 100


class VehicleCreate100(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    success_url = '/admin-tables/'
    model = VehicleDetailsAbove100
    fields = '__all__'
    template_name = 'admin-veh_create(100).html'


class VehicleUpdate100(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = VehicleDetailsAbove100
    success_url = '/admin-tables/'
    fields = '__all__'
    template_name = 'admin-veh_update(100).html'


class VehicleDelete100(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = VehicleDetailsAbove100
    success_url = '/admin-tables/'
    template_name = 'admin-veh_delete(100).html'

#corporate fareprice
@login_required(login_url='admin_login')
def corporate_fareprice(request):
    if request.method == 'POST':
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['VechicleType']
        # ---Map API--
        gmaps = googlemaps.Client(key='AIzaSyCqM7uF9c0ZMQjdssHqSMJJ3mBcmz5RNS0')
        my_dist = gmaps.distance_matrix(sour, dest)['rows'][0]['elements'][0]

        database_dist = my_dist['distance']['text']
        database_time = my_dist['duration']['text']

        km = my_dist['distance']['text'].split(" ")[0]
        total_dist1 = re.sub(',', "", km)

        conv_dist1 = float(total_dist1)
        
        # for 0 - 30
        v = [i.vehicle_Corporate for i in Corporate_Fare_Price.objects.all()]
        bp = [i.vehicle_Base_Price for i in Corporate_Fare_Price.objects.all()]
        perkm = [i.per_km_Corporate for i in Corporate_Fare_Price.objects.all()]

        # for 0 - 30
        if bvehicle == v[0]:
            base_fare = bp[0]
            per_km = perkm[0]
            
        elif bvehicle == v[1]:
            base_fare = bp[1]
            per_km = perkm[1]
            
        elif bvehicle == v[2]:
            base_fare = bp[2]
            per_km = perkm[2]

        elif bvehicle == v[3]:
            base_fare = bp[3]
            per_km = perkm[3]

        # for 0 - 30
        if (conv_dist1 > 2.5 and conv_dist1 <= 30):
            if bvehicle.lower() == 'auto':
                driver_fare = ((conv_dist1 * per_km) + base_fare)

            elif bvehicle.lower() == 'tata ace':
                driver_fare = ((conv_dist1 * per_km) + base_fare)

            elif bvehicle.lower() == 'small pickup':
                driver_fare = ((conv_dist1 * per_km) + base_fare)

            elif bvehicle.lower() == 'large pickup':
                driver_fare = ((conv_dist1 * per_km) + base_fare)

        # for upto 30
        if (conv_dist1 > 30):
            if bvehicle.lower() == 'auto':
                driver_fare = (2 * conv_dist1 * per_km) + base_fare

            elif bvehicle.lower() == 'tata ace':
                driver_fare = (2 * conv_dist1 * per_km) + base_fare

            elif bvehicle.lower() == 'small pickup':
                driver_fare = (2 * conv_dist1 * per_km) + base_fare

            elif bvehicle.lower() == 'large pickup':
                driver_fare = (2 * conv_dist1 * per_km) + base_fare

            else:
                driver_fare = (2 * conv_dist1 * per_km) + base_fare

        estimate = "{:.2f}".format(driver_fare)
        
        context = {
            'to': sour,
            'from': dest,
            'VechicleType': bvehicle,
            'distance': database_dist,
            'duration': database_time,
            'TotalCost': estimate,
        }
        return render(request, 'admin-corporate-invoice.html', context)
    corp = Corporate_Fare_Price.objects.all()
    context1 = {'corp': corp}
    return render(request, 'admin-corporate.html',context1)

class CorporateCreate(LoginRequiredMixin, CreateView):
    login_url = '/admin-login/'
    success_url = '/admin-corporate/'
    model = Corporate_Fare_Price
    fields = '__all__'
    template_name = 'admin-corporate_create.html'

class CorporateUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin-login/'
    model = Corporate_Fare_Price
    success_url = '/admin-corporate/'
    fields = '__all__'
    template_name = 'admin-corporate_update.html'

class CorporateDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin-login/'
    model = Corporate_Fare_Price
    success_url = '/admin-corporate/'
    template_name = 'admin-corporate_delete.html'