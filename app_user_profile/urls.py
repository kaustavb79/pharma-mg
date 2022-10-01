from django.urls import path, re_path
from app_user_profile import views

app_name = 'app_user_profile'

urlpatterns = [
    path('', views.home, name='home'),    
    path(r'generate/', views.GenerateOTP.as_view(), name="generate"),
    path(r'validate/', views.ValidateOTP.as_view(), name="validate"),

]
