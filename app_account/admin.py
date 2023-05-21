from django.contrib import admin
from .models import *


class ProfileAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class OtpVerifyAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


class AddressAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('date_time',)


admin.site.register(Profile, ProfileAdminReadOnly)
admin.site.register(OtpVerify, OtpVerifyAdminReadOnly)
admin.site.register(Address, AddressAdminReadOnly)
