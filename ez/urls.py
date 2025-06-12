"""ez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from eztruck import urls
admin.site.site_header = "ezTruck Admin"
admin.site.site_title = "ezTruck Admin Portal"
admin.site.index_title = "Welcome to ezTruck Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)), # eztruck.urls
    path('adminpanel/',include('ezadmin.urls')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'eztruck.views.error'
handler500 = 'eztruck.views.error'
handler403 = 'eztruck.views.error'
handler400 = 'eztruck.views.error'
