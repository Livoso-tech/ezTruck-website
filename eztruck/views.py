import re
from django.shortcuts import render
from .models import drivers_details,ContactUs,CareerApply,Enterprice,Bookings
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView
from ezadmin.models import VehicleDetails,VehicleDetails50_100,VehicleDetailsAbove100
# from geopy.geocoders import Nominatim
import googlemaps
# Create your views here.
@csrf_protect
def index(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        #---Map API--
        gmaps = googlemaps.Client(key='AIzaSyCqM7uF9c0ZMQjdssHqSMJJ3mBcmz5RNS0')
        my_dist = gmaps.distance_matrix(sour,dest)['rows'][0]['elements'][0]
        
        database_dist = my_dist['distance']['text']
        database_time = my_dist['duration']['text']
        
        
        km = my_dist['distance']['text'].split(" ")[0]
        total_dist1 = re.sub(',',"",km)
        total_time1 = my_dist['duration']['value']
        
        conv_dist1 = float(total_dist1)
        minutes = total_time1 // 60
        #for 0 - 30
        bp = [i.price for i in VehicleDetails.objects.all()]
        perkm = [i.per_km for i in VehicleDetails.objects.all()]
        permin = [i.rate_per_min for i in VehicleDetails.objects.all()]
        waiting = [i.waiting_charge for i in VehicleDetails.objects.all()]
        v = [i.vehicle for i in VehicleDetails.objects.all()]
        
        #for 30-99
        bp99 = [i.price50 for i in VehicleDetails50_100.objects.all()]
        perkm99 = [i.per_km50 for i in VehicleDetails50_100.objects.all()]
        v99 = [i.vehicle50 for i in VehicleDetails50_100.objects.all()]
        
        #for above 100
        perkm100 = [i.per_km100 for i in VehicleDetailsAbove100.objects.all()]
        v100 = [i.vehicle100 for i in VehicleDetailsAbove100.objects.all()]
        
        #for 0 - 30
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
            
        #for 30-99    
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
            
        #for above 100
        if bvehicle == v100[0]:
            per_km100 = perkm100[0]
        elif bvehicle == v100[1]:
            per_km100 = perkm100[1]
        elif bvehicle == v100[2]:
            per_km100 = perkm100[2]
        elif bvehicle == v100[3]:
            per_km100 = perkm100[3]
        
        #for 0 - 30   
        if (conv_dist1 > 2.5 and conv_dist1 <= 30):
            if bvehicle.lower() == 'auto' and minutes >= wait_chrg:
                driver_fare = ((conv_dist1 * per_km) + ((minutes - wait_chrg) * per_min) + base_fare)

            elif bvehicle.lower() == 'tata ace' and minutes >= wait_chrg:
                driver_fare = ((conv_dist1 * per_km) + ((minutes - wait_chrg) * per_min) + base_fare)

            elif bvehicle.lower() == 'small pickup' and minutes >= wait_chrg:
                driver_fare = ((conv_dist1 * per_km) + ((minutes - wait_chrg) * per_min) + base_fare)

            elif bvehicle.lower() == 'large pickup' and minutes >= wait_chrg:
                driver_fare = ((conv_dist1 * per_km) + ((minutes - wait_chrg) * per_min) + base_fare)

            else:
                driver_fare = ((conv_dist1 * per_km) + base_fare)
        
        #for 30-99   
        if (conv_dist1 > 30 and conv_dist1 <= 99):
            if bvehicle.lower() == 'auto':
                driver_fare = (2 * conv_dist1 * per_km99) +  base_fare99

            elif bvehicle.lower() == 'tata ace':
                driver_fare = (2 * conv_dist1 * per_km99) +  base_fare99

            elif bvehicle.lower() == 'small pickup':
                driver_fare = (2 * conv_dist1 * per_km99) +  base_fare99

            elif bvehicle.lower() == 'large pickup':
                driver_fare = (2 * conv_dist1 * per_km99) +  base_fare99

            else:
                driver_fare = (2 * conv_dist1 * per_km99) +  base_fare99
        
        #for above 100    
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
        #---Map API End----
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle,distance=database_dist,durations=database_time,total_price=estimate)
        ob.save()
        
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['amitav@livosotech.com'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
        return render(request, 'priceCalculator.html',{'ob':ob})
    booking = Bookings.objects.all().count()
    return render(request, 'index.html', {'booking':booking})

def price(request):
    return render(request , 'priceCalculator.html')

@csrf_protect
def about(request):
    try:
        booking = Bookings.objects.all().count()
        return render(request,'about.html',{'booking':booking})
    except:
        return render(request, 'index.html')
        
def services(request):
    return render(request,'services.html')

@csrf_protect
def driver(request):
    if request.method == 'POST':
        demail = request.POST['e1']
        drivername = request.POST['dname']
        drivernumber = request.POST['dnum']
        dcity = request.POST['citys']
        licnumber = request.POST['licnum']
        vehnumber = request.POST['vehnum']
        dvehicle = request.POST['veh']
       
        ob = drivers_details.objects.create(email= demail, driver_name = drivername, driver_number=drivernumber,city = dcity, lic_number= licnumber, veh_number=vehnumber,vehicle=dvehicle)
        ob.save()
        recipient_list = [demail]
        mess = render_to_string('driver_mail.html',{"D_name":drivername,"D_mail":demail,"D_phone":drivernumber,"D_city":dcity,"D_lic":licnumber,"D_vic_num":vehnumber,"D_type_veh":dvehicle})
        sendmess = render_to_string('driver_mail_success.html',{"D_name":drivername,"D_mail":demail,"D_phone":drivernumber,"D_city":dcity,"D_lic":licnumber,"D_vic_num":vehnumber,"D_type_veh":dvehicle})
        send_mail(drivername,dvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Thankyou',dvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
        total_driver = drivers_details.objects.all().count()
        return render(request,"index.html",{'total_driver':total_driver})
    return render(request,'driver.html')

@csrf_protect
def enterprise(request):
    if request.method == 'POST':
        en = request.POST['entrname']
        e_mail = request.POST['entremail']
        e_num = request.POST['entrnum']
        e_city = request.POST['entrcitys']
        e_comp = request.POST['entrcomp']
        e_licnum = request.POST['entrlicnum']
        e_vehnum = request.POST['entrpvehnum']
        e_veh = request.POST['entrveh']
           
        ob = Enterprice.objects.create(Enterp_name=en,Enterp_email=e_mail,Enterp_num=e_num, Company=e_comp,Enterp_city=e_city,Enterp_lic_number=e_licnum ,Enterp_veh_number=e_vehnum,Enterp_vehicle=e_veh)
        ob.save()
        recipient_list = [e_mail]
        mess = render_to_string('Enterprice_mail.html',{"En_name":en,"En_mail":e_mail,"En_phone":e_num,"En_comp_name":e_comp,"En_city":e_city,"En_licnum":e_licnum,"En_vehnum":e_vehnum,"En_vech":e_veh})
        sendmess = render_to_string('Enterprise_success_mail.html',{"En_name":en,"En_mail":e_mail,"En_phone":e_num,"En_comp_name":e_comp,"En_city":e_city,"En_licnum":e_licnum,"En_vehnum":e_vehnum,"En_vech":e_veh})
        send_mail(e_comp,e_city,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Thankyou',e_comp,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
        return render(request,'enterprise.html')
    total_driver = drivers_details.objects.all().count()
    return render(request,'enterprise.html',{'total_driver':total_driver})

@csrf_protect
def contact(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'contact.html')
    return render(request,'contact.html')
def FAQ(request):
    return render(request,'FAQ.html')
def help(request):
    return render(request,'help.html')
    
def error(request,exception=None):
    return render(request,'index.html')
 
def termANDconditions(request):
    return render(request,'termANDconditions.html')
def team(request):
    return render(request,'team.html')
def news(request):
    return render(request,'news.html')
def blog(request):
    return render(request,'blog.html')
def raisingFuelPrice(request):
    return render(request,'raisingFuelPrice.html')
def logisticsRends(request):
    return render(request,'logisticsRends.html')
def supplyChain(request):
    return render(request,'supplyChain.html')
def privacy(request):
    return render(request,'privacy-policy.html')

def refundcancellation(request):
    return render(request,'refund-cancellation-policy.html')

def shipdelivery(request):
    return render(request,'ship-delivery.html')




# @csrf_protect
# def applyForm(request):
#     if request.method == 'POST':
#         fn = request.POST['first_name']
#         ln = request.POST['last_name']
#         date = request.POST['birthday']
#         gen = request.POST['gender']
#         amail = request.POST['email']
#         phn = request.POST['phone']
#         pos = request.POST['subject']
#         loc = request.POST['location']
#         addr = request.POST['ad']
#         file = request.FILES['myfile']
#         ob = CareerApply.objects.create(fname= fn, lname = ln, dob=date, gender= gen, app_email=amail,app_phone=phn, position=pos,location=loc,address=addr,document=file)
#         ob.save()
#         return render(request,"career.html",{'output':"register success"})
#     return render(request,'applyForm.html')

def LocalLogistics(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'LocalLogistics.html')
    return render(request,'LocalLogistics.html')
def HouseShifting(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'HouseShifting.html')
    return render(request,'HouseShifting.html')
def constructionMaterials(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'constructionMaterials.html')
    return render(request,'constructionMaterials.html')
def MoversPacker(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'MoversPacker.html')
    return render(request,'MoversPacker.html')

def businessLogistics(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'businessLogistics.html')
    return render(request,'businessLogistics.html')


def TransportionServices(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'TransportionServices.html')
    return render(request,'TransportionServices.html')



def EcommerceLogistics(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'EcommerceLogistics.html')
    return render(request,'EcommerceLogistics.html')
def FurnitureLogistics(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'FurnitureLogistics.html')
    return render(request,'FurnitureLogistics.html')
def MiningLogistics(request):
    if request.method == "POST":
        Coname = request.POST['Cname']
        Comail = request.POST['Cmail']
        Cophn = request.POST['Cphone']
        Cosub = request.POST['Csubject']
        Comsg = request.POST['Cmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":Coname,"C_mail":Comail,"C_phone":Cophn,"C_msg":Comsg})
        send_mail(Cosub,Comsg,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=Coname,Umail=Comail,Uphn=Cophn,Usub=Cosub,Umsg=Comsg)
        Us.save()
        return render(request,'MiningLogistics.html')
    return render(request,'MiningLogistics.html')

@csrf_protect
def sasmitanjali(request):
    if request.method == "POST":
        ssname = request.POST['sasname']
        ssmail = request.POST['sasmail']
        ssphn = request.POST['sasphone']
        sssub = request.POST['sassubject']
        ssmsg = request.POST['sasmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":ssname,"C_mail":ssmail,"C_phone":ssphn,"C_msg":ssmsg})
        send_mail('Contact-Details',ssmsg,settings.EMAIL_HOST_USER,['sasmitanjali@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=ssname,Umail=ssmail,Uphn=ssphn,Usub=sssub,Umsg=ssmsg)
        Us.save()
        return render(request,'index.html')
    return render(request,'sasmitanjali.html')

@csrf_protect
def kalirath(request):
    if request.method == "POST":
        klname = request.POST['kalname']
        klmail = request.POST['kalmail']
        klphn = request.POST['kalphone']
        klsub = request.POST['kalsubject']
        klmsg = request.POST['kalmessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":klname,"C_mail":klmail,"C_phone":klphn,"C_msg":klmsg})
        send_mail('Contact-Details',klmsg,settings.EMAIL_HOST_USER,['kalirath@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=klname,Umail=klmail,Uphn=klphn,Usub=klsub,Umsg=klmsg)
        Us.save()
        return render(request,'index.html')
    return render(request,'kalirath.html')

@csrf_protect
def ellora(request):
    if request.method == "POST":
        elname = request.POST['elloname']
        elmail = request.POST['ellomail']
        elphn = request.POST['ellophone']
        elsub = request.POST['ellosubject']
        elmsg = request.POST['ellomessage']
        mess = render_to_string('contact_us_mail.html',{"C_name":elname,"C_mail":elmail,"C_phone":elphn,"C_msg":elmsg})
        send_mail('Contact-Details',elmsg,settings.EMAIL_HOST_USER,['ellora@eztruck.co'],html_message=mess)
        Us = ContactUs.objects.create(Uname=elname,Umail=elmail,Uphn=elphn,Usub=elsub,Umsg=elmsg)
        Us.save()
        return render(request,'index.html')
    return render(request,'ellora.html')

@csrf_protect
def bhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'bhubaneswar.html')






@csrf_protect
def logisticsbhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'logisticsbhubaneswar.html')

@csrf_protect
def logisticscuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'logisticscuttack.html')

@csrf_protect
def logisticsberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'logisticsberhampur.html')











@csrf_protect
def cuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'cuttack.html')



@csrf_protect
def berhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
         
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'berhampur.html')
def contact_us_mail(request):
    return render(request,'contact_us_mail.html')









@csrf_protect
def transportbhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'transportbhubaneswar.html')


@csrf_protect
def transportcuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'transportcuttack.html')


@csrf_protect
def transportberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'transportberhampur.html')









@csrf_protect
def constructionbhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'constructionbhubaneswar.html')


@csrf_protect
def constructioncuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'constructioncuttack.html')


@csrf_protect
def constructionberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'constructionberhampur.html')











@csrf_protect
def businesslogisticsbhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'businesslogisticsbhubaneswar.html')


@csrf_protect
def businesslogisticscuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'businesslogisticscuttack.html')


@csrf_protect
def businesslogisticsberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'businesslogisticsberhampur.html')









@csrf_protect
def furniturebhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'furniturebhubaneswar.html')


@csrf_protect
def furniturecuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'furniturecuttack.html')


@csrf_protect
def furnitureberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'furnitureberhampur.html')










@csrf_protect
def mininglogisticsbhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'mininglogisticsbhubaneswar.html')


@csrf_protect
def mininglogisticscuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'mininglogisticscuttack.html')


@csrf_protect
def mininglogisticsberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'mininglogisticsberhampur.html')











@csrf_protect
def ecommercebhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'ecommercebhubaneswar.html')


@csrf_protect
def ecommercecuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'ecommercecuttack.html')


@csrf_protect
def ecommerceberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'ecommerceberhampur.html')








@csrf_protect
def houseshiftingbhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'houseshiftingbhubaneswar.html')


@csrf_protect
def houseshiftingcuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'houseshiftingcuttack.html')


@csrf_protect
def houseshiftingberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'houseshiftingberhampur.html')









@csrf_protect
def packersmoversbhubaneswar(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'packersmoversbhubaneswar.html')


@csrf_protect
def packersmoverscuttack(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'packersmoverscuttack.html')


@csrf_protect
def packersmoversberhampur(request):
    if request.method == 'POST':
        bn = request.POST['bname']
        bmail = request.POST['bemail']
        bphn = request.POST['bnum']
        sour = request.POST['deliverycity']
        dest = request.POST['departurecity']
        bvehicle = request.POST['ftype']
        
        ob = Bookings.objects.create(Bname=bn,Bemail=bmail,Bphone=bphn, source=sour,destination=dest,truck=bvehicle)
        ob.save()
        recipient_list = [bmail]
        mess = render_to_string('bookingMail.html',{"B_name":bn,"B_mail":bmail,"B_phone":bphn,"Source":sour,"Destination":dest,"vich":bvehicle})
        sendmess = render_to_string('bookingSuccessfulMail.html',{"B_name":bn})
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,['it.dev@eztruck.co'],html_message=mess)
        send_mail('Bookings',bvehicle,settings.EMAIL_HOST_USER,recipient_list,html_message=sendmess)
    return render(request,'packersmoversberhampur.html')
















@csrf_protect   
def bookingMail(request):
    booking_mail = Bookings.objects.all()
    return render(request,'bookingMail.html', {'bookings':booking_mail})

#eztruck all CareerApply
def career(request):
    return render(request,'career.html')
def apply(request):
    return render(request,'apply.html')
class adminManager(CreateView):
    model = CareerApply
    fields = '__all__'
    template_name = 'adminManager.html'
    success_url = '/career/apply/'
# def adminManager(request):
#     return render(request,'adminManager.html')
class marKeting(CreateView):
    model = CareerApply
    fields = '__all__'
    template_name = 'marketing.html'
    success_url = '/career/apply/'
# def marketing(request):
#     return render(request,'marketing.html')
class opeRation(CreateView):
    model = CareerApply
    fields = '__all__'
    template_name = 'operation.html'
    success_url = '/career/apply/'
# def operation(request):
#     return render(request,'operation.html')
class opeRation(CreateView):
    model = CareerApply
    fields = '__all__'
    template_name = 'operation.html'
    success_url = '/career/apply/'
# def digital(request):
#     return render(request,'digital.html')
class diGital(CreateView):
    model = CareerApply
    fields = '__all__'
    template_name = 'digital.html'
    success_url = '/career/apply/'
# def backend(request):
#     return render(request,'backend.html')
class bacKend(CreateView):
    model = CareerApply
    fields = '__all__'
    template_name = 'backend.html'
    success_url = '/career/apply/'
# def business(request):
#     return render(request,'business.html')
class busiNess(CreateView):
    model = CareerApply
    fields = '__all__'
    template_name = 'business.html'
    success_url = '/career/apply/'



def logisticautomation(request):
    return render(request,'LogisticAutomation.html')


def the5Psoflogistics(request):
    return render(request,'the-5Ps-of-logistics.html')

