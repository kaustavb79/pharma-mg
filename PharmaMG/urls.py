"""
URL configuration for PharmaMG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app_account.views import home_view, business_login, business_logout, register_user_ajax, \
    patient_login, patient_logout

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name="home"),
    path('bui_login/', business_login, name="bui_login"),
    path('bui_logout/', business_logout, name="bui_logout"),

    path('register_user_ajax/', register_user_ajax, name="send_otp"),
    path('patient_login/', patient_login, name="patient_login"),
    path('patient_logout/', patient_logout, name="patient_logout"),


    path('pharma-mg/', include(('app_pharma_mg.urls','app_pharma_mg'), namespace='pharmamg')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
