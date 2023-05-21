from django.urls import path

from app_pharma_mg.views import dashboard_view

urlpatterns = [
    path('dashboard', dashboard_view, name="dashboard"),
]