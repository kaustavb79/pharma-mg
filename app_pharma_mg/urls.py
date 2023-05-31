from django.urls import path

from app_pharma_mg import cart_views
from app_pharma_mg.cart_views import order_detail
from app_pharma_mg.views import *

urlpatterns = [
    # BUI urls
    path('bui_dashboard/', dashboard_view, name="dashboard"),

    # pharmacy urls for admin user
    path('bui_manage_pharmacy/', manage_pharmacy_view, name="manage_pharmacy"),
    path('bui_add_pharmacy/', add_pharmacy, name="add_pharmacy"),
    path('edit_form_ajax/', edit_form_ajax, name="edit_form_ajax"),
    path('bui_delete_pharmacy/<str:pharmacy_id>/', delete_pharmacy_ajax, name="delete_pharmacy"),

    # clinic urls for admin user
    path('bui_manage_clinic/', manage_clinic_view, name="manage_clinic"),
    path('bui_add_clinic/', add_clinic, name="add_clinic"),
    path('edit_clinic_form_ajax/', edit_form_ajax, name="edit_clinic_form_ajax"),
    path('bui_delete_clinic/<str:clinic_id>/', delete_pharmacy_ajax, name="delete_clinic"),


    # PHARMACY USER urls
    path('bui_pharmacy_dashboard/', dashboard_pharmacy_view, name="pharmacy_dashboard"),
    path('bui_pharmacy_users/', manage_pharmacy_user_view, name="manage_pharmacy_users"),
    path('bui_pharmacy_users_delete/<str:user_id>/', delete_pharmacy_employee_ajax, name="delete_pharmacy_employee"),
    path('bui_add_pharmacy_user/', add_pharmacy_employee, name="add_pharmacy_employee"),
    path('bui_pharmacy_products/', manage_pharmacy_products_view, name="manage_pharmacy_products"),
    path('bui_pharmacy_edit_product_form_ajax/', edit_product_form_ajax, name="edit_product_form_ajax"),
    path('bui_add_pharmacy_product/', add_pharmacy_product, name="add_pharmacy_product"),
    path('bui_create_order_pharmacy_view/', create_order_pharmacy_view, name="create_order_pharmacy_view"),
    path('bui_create_order_ajax/', create_order_ajax, name="create_order_ajax"),
    path('bui_manage_pharmacy_orders_view/', manage_pharmacy_orders_view, name="manage_pharmacy_orders_view"),

    # CLINIC USER urls
    path('bui_clinic_dashboard/', dashboard_clinic_view, name="clinic_dashboard"),
    path('bui_clinic_users/', manage_clinic_user_view, name="manage_clinic_users"),
    path('bui_clinic_users_delete/<str:user_id>/', delete_clinic_employee_ajax, name="delete_clinic_employee"),
    path('bui_add_clinic_user/', add_clinic_employee, name="add_clinic_employee"),
    path('bui_schedule_consultation_view/', schedule_consultation_view, name="schedule_consultation_view"),
    path('bui_schedule_consultation_ajax/', schedule_consultation_ajax, name="schedule_consultation_ajax"),
    path('bui_manage_consultation_view/', manage_consultation_view, name="manage_consultation_view"),


    # PATIENT/CUSTOMER urls
    path('patient_home/', patient_home, name="patient_home"),
    path('order_detail/', order_detail, name="order_detail"),

    # CART URLS
    path('cart/add/<str:id>/', cart_views.cart_add, name='cart_add'),
    path('cart/item_clear/<str:id>/', cart_views.item_clear, name='item_clear'),
    path('cart/item_increment/<str:id>/',
         cart_views.item_increment, name='item_increment'),
    path('cart/item_decrement/<str:id>/',
         cart_views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_views.cart_detail,name='cart_detail'),
    path('cart/checkout/',cart_views.checkout,name='checkout'),


]