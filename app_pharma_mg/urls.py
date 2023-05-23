from django.urls import path

from app_pharma_mg.views import *

urlpatterns = [
    # BUI urls
    path('bui_dashboard/', dashboard_view, name="dashboard"),
    path('bui_manage_pharmacy/', manage_pharmacy_view, name="manage_pharmacy"),
    path('bui_add_pharmacy/', add_pharmacy, name="add_pharmacy"),
]