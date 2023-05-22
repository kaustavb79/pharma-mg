from django.contrib import admin
from .models import *


class PharmacyProfileAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class PharmacyUsersAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


admin.site.register(Pharmacy, PharmacyProfileAdminReadOnly)
admin.site.register(PharmacyUsers, PharmacyUsersAdminReadOnly)
