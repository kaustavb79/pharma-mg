from django.contrib import admin

# Register your models here.
from .models import PhoneToken,Profile

class ProfileAdminReadOnly(admin.ModelAdmin):
    readonly_fields = ('updated_at','created_at',)
    list_display = (
        'user',
        'gender',
        'role',
        'blood_group',
    )

    list_filter = (
        'role',
        'service',
        'gender',
        'blood_group',
    )


class PhoneTokenAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'timestamp', 'attempts', 'used')
    search_fields = ('phone_number', )
    list_filter = ('timestamp', 'attempts', 'used')
    readonly_fields = ('phone_number', 'otp', 'timestamp', 'attempts')


admin.site.register(Profile, ProfileAdminReadOnly)
admin.site.register(PhoneToken, PhoneTokenAdmin)