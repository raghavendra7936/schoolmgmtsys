"""schoolmgmtsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    #path('admin/', admin.site.urls),
    path('', include('apps.common.urls')),    
    path('student/', include('apps.student.urls')),
    path('result/', include('apps.result.urls')), 
    path('staff/', include('apps.staff.urls')),
    path('invoice/', include('apps.invoice.urls')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
