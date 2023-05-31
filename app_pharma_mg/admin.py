from django.contrib import admin

from .models import *


class PharmacyProfileAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class PharmacyUsersAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class ClinicAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class ClinicUsersAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class PrescriptionAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class TransactionAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class OrderAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class ConsultationAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class ItemAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time', 'item_id', 'pharmacy', 'updated_on',)


admin.site.register(Pharmacy, PharmacyProfileAdminReadOnly)
admin.site.register(PharmacyUsers, PharmacyUsersAdminReadOnly)
admin.site.register(Clinic, ClinicAdminReadOnly)
admin.site.register(ClinicUsers, ClinicUsersAdminReadOnly)
admin.site.register(Item, ItemAdminReadOnly)
admin.site.register(Prescription, PrescriptionAdminReadOnly)
admin.site.register(Transaction, TransactionAdminReadOnly)
admin.site.register(Order, OrderAdminReadOnly)
admin.site.register(Consultation, ConsultationAdminReadOnly)
