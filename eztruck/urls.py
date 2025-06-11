from django.urls import path
from eztruck import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView
from .views import adminManager,opeRation,diGital,marKeting,bacKend,busiNess

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewsSitemap

sitemaps = {
    'static': StaticViewsSitemap,
}

urlpatterns = [
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path('',views.index, name='index'),
    #all eztruck Services
    path('logistics-services/',views.services, name='services'),
    path('mining-logistics-services/',views.MiningLogistics, name='MiningLogistics'),
    path('local-logistics-services/',views.LocalLogistics, name='LocalLogistics'),
    path('packers-movers-services/',views.MoversPacker, name='MoversPacker'),
    path('house-shifting-services/',views.HouseShifting, name='HouseShifting'),
    path('construction-materials-logistics/',views.constructionMaterials, name='constructionMaterials'),
    path('business-logistics-services/',views.businessLogistics, name='businessLogistics'),
    path('ecommerce-logistics-services/',views.EcommerceLogistics, name='EcommerceLogistics'),
    path('furniture-logistics-services/',views.FurnitureLogistics, name='FurnitureLogistics'),
    path('transportation-services/',views.TransportionServices, name='TransportionServices'),
    #driver and enterprise urls
    path('logistics-partners/',views.driver, name='driver'),
    path('enterprise-logistics-services/',views.enterprise, name='enterprise'),
    #all team ContactUs
    path('contact/',views.contact, name='contact'),
    #all urls of eztruck    
    path('blog/',views.blog, name='blog'),
    path('blog/Increasing-fuel-price-affecting-Logistics-Industry-in-India/',views.raisingFuelPrice, name='raisingFuelPrice'),
    path('blog/trends-logistics-supply-chain/',views.logisticsRends, name='logisticsRends'),
    path('blog/covid-19-affected-supply-chains-and-what-comes-Next/',views.supplyChain, name='supplyChain'),

    path('blog/logistic-automation/',views.logisticautomation, name='logisticautomation'),

    path('blog/the-5Ps-of-logistics/',views.the5Psoflogistics, name='the5Psoflogistics'),

    path('term-conditions/',views.termANDconditions, name='termANDconditions'),
    path('logistics-updates/',views.news, name='news'),  
    path('about/',views.about, name='about'),
    path('logistics-service-in-bhubaneswar/',views.bhubaneswar, name='bhubaneswar'),
    path('logistics-service-in-cuttack/',views.cuttack, name='cuttack'),
    path('logistics-service-in-berhampur/',views.berhampur, name='berhampur'),



    path('logistics-service-bhubaneswar/',views.logisticsbhubaneswar, name='logisticsbhubaneswar'),
    path('logistics-service-cuttack/',views.logisticscuttack, name='logisticscuttack'),
    path('logistics-service-berhampur/',views.logisticsberhampur, name='logisticsberhampur'),
  

    path('transportation-service-in-bhubaneswar/',views.transportbhubaneswar, name='transportbhubaneswar'),
    path('transportation-service-in-cuttack/',views.transportcuttack, name='transportcuttack'),
    path('transportation-service-in-berhampur/',views.transportberhampur, name='transportberhampur'),


    path('construction-material-logistics-in-bhubaneswar/',views.constructionbhubaneswar, name='constructionbhubaneswar'),
    path('construction-material-logistics-in-cuttack/',views.constructioncuttack, name='constructioncuttack'),
    path('construction-material-logistics-in-berhampur/',views.constructionberhampur, name='constructionberhampur'),


    path('business-logistics-in-bhubaneswar/',views.businesslogisticsbhubaneswar, name='businesslogisticsbhubaneswar'),
    path('business-logistics-in-cuttack/',views.businesslogisticscuttack, name='businesslogisticscuttack'),
    path('business-logistics-in-berhampur/',views.businesslogisticsberhampur, name='businesslogisticsberhampur'),


    path('furniture-logistics-in-bhubaneswar/',views.furniturebhubaneswar, name='furniturebhubaneswar'),
    path('furniture-logistics-in-cuttack/',views.furniturecuttack, name='furniturecuttack'),
    path('furniture-logistics-in-berhampur/',views.furnitureberhampur, name='furnitureberhampur'),

    path('mining-logistics-in-bhubaneswar/',views.mininglogisticsbhubaneswar, name='mininglogisticsbhubaneswar'),
    path('mining-logistics-in-cuttack/',views.mininglogisticscuttack, name='mininglogisticscuttack'),
    path('mining-logistics-in-berhampur/',views.mininglogisticsberhampur, name='mininglogisticsberhampur'),

    path('e-commerce-logistics-in-bhubaneswar/',views.ecommercebhubaneswar, name='ecommercebhubaneswar'),
    path('e-commerce-logistics-in-cuttack/',views.ecommercecuttack, name='ecommercecuttack'),
    path('e-commerce-logistics-in-berhampur/',views.ecommerceberhampur, name='ecommerceberhampur'),

    path('house-shifting-logistics-company-in-bhubaneswar/',views.houseshiftingbhubaneswar, name='houseshiftingbhubaneswar'),
    path('house-shifting-logistics-company-in-cuttack/',views.houseshiftingcuttack, name='houseshiftingcuttack'),
    path('house-shifting-logistics-company-in-berhampur/',views.houseshiftingberhampur, name='houseshiftingberhampur'),

    path('packers-and-movers-company-in-bhubaneswar/',views.packersmoversbhubaneswar, name='packersmoversbhubaneswar'),
    path('packers-and-movers-company-in-cuttack/',views.packersmoverscuttack, name='packersmoverscuttack'),
    path('packers-and-movers-company-in-berhampur/',views.packersmoversberhampur, name='packersmoversberhampur'),


    path('logistics-faq/',views.FAQ, name='FAQ'),
    path('help-center/',views.help, name='help'),
    #eztruck all CareerApply
    path('career/',views.career, name='career'),
    path('career/apply/',views.apply, name='apply'),
    path('admin-Manager/',adminManager.as_view(), name='adminManager'),
    path('marketing/',marKeting.as_view(), name='marketing'),
    path('operation/',opeRation.as_view(), name='operation'),
    path('digital/',diGital.as_view(), name='digital'),
    path('backend/',bacKend.as_view(), name='backend'),
    path('business/',busiNess.as_view(), name='business'),
    path('privacy-policy',views.privacy, name='privacy'),
    path('refund-cancellation-policy',views.refundcancellation, name='refundcancellation'),
    path('ship-delivery',views.shipdelivery, name='shipdelivery'),
    #all extra urls
    path('error/',views.error, name='error'),
    #SiteMaps
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap')
    
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
