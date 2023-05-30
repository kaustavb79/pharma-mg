import uuid
from django.contrib.auth.models import User
from django.db import models

ROLES = (
    ('admin', 'ADMIN'),
    ('patient', 'PATIENT'),
    ('doctor', 'DOCTOR'),
    ('pharmacist', 'PHARMACIST'),
    ('receptionist', 'RECIPTIONIST')
)


class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(blank=True, null=True, choices=ROLES,max_length=100)

    phone = models.CharField(blank=True, null=True,max_length=15)
    email = models.CharField(blank=True, null=True,max_length=200)

    first_name = models.CharField(blank=True, null=True,max_length=200)
    last_name = models.CharField(blank=True, null=True,max_length=200)
    user_address = models.TextField(blank=True, null=True)

    is_mobile_verified = models.BooleanField(default=False)

    profile_pic = models.FileField(blank=True,null=True,upload_to="app_pharmamg/profile_images/")

    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.profile_id}"


class OtpVerify(models.Model):
    otp_sid = models.CharField(primary_key=True, default="",max_length=200)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    status = models.CharField(blank=True, null=True,max_length=100)
    otp = models.CharField(blank=True, null=True,max_length=10)
    is_verified = models.BooleanField(default=False)
    has_expired = models.BooleanField(default=False)

    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.otp_sid}"


class Address(models.Model):
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    city = models.CharField(blank=True, null=True,max_length=200)
    state = models.CharField(blank=True, null=True,max_length=200)
    country = models.CharField(blank=True, null=True, default="INDIA",max_length=200)
    pincode = models.CharField(blank=True, null=True,max_length=20)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.address_id}"
