from django.contrib import sitemaps
from django.urls import reverse

class StaticViewsSitemap(sitemaps.Sitemap):

    priority = 0.5
    changefreq = "daily"
    protocol = 'https'

    def items(self):
        return [
            'index',
            'services',
            'driver',
            'contact',
            'about',
            'MiningLogistics',
            'LocalLogistics',
            'MoversPacker',
            'HouseShifting',
            'constructionMaterials',
            'businessLogistics',
            'EcommerceLogistics',
            'FurnitureLogistics',
            'transportbhubaneswar',
            'transportcuttack',
            'transportberhampur',
            'constructionbhubaneswar',
            'constructioncuttack',
            'constructionberhampur',
            'businesslogisticsbhubaneswar',
            'businesslogisticscuttack',
            'businesslogisticsberhampur',
            'furniturebhubaneswar',
            'furniturecuttack',
            'furnitureberhampur',
            'mininglogisticsbhubaneswar',
            'mininglogisticscuttack',
            'mininglogisticsberhampur',
            'ecommercebhubaneswar',
            'ecommercecuttack',
            'ecommerceberhampur',
            'houseshiftingbhubaneswar',
            'houseshiftingcuttack',
            'houseshiftingberhampur',
            'packersmoversbhubaneswar',
            'packersmoverscuttack',
            'packersmoversberhampur',
            'TransportionServices',
            'enterprise',
            'blog',
            'termANDconditions',
            'news',
            'bhubaneswar',
            'berhampur',
            'FAQ',
            'help',
            'career',
            'apply',
        ]

    def location(self,item):
        return reverse(item)
