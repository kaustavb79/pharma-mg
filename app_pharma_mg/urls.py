from django.urls import path

from app_pharma_mg.views import *

urlpatterns = [
    # BUI urls
    path('bui_dashboard/', dashboard_view, name="dashboard"),
    path('bui_manage_pharmacy/', manage_pharmacy_view, name="manage_pharmacy"),
    path('bui_add_pharmacy/', add_pharmacy, name="add_pharmacy"),
    path('edit_form_ajax/', edit_form_ajax, name="edit_form_ajax"),
    path('bui_delete_pharmacy/<str:pharmacy_id>/', delete_pharmacy_ajax, name="delete_pharmacy"),
]