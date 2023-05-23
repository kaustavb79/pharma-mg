import uuid
from django.db import models

from app_account.models import Profile


class Pharmacy(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    added_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    name = models.CharField(blank=True, null=True, max_length=200)
    address = models.TextField(blank=True, null=True)

    store_phone = models.CharField(blank=True, null=True, max_length=15)
    store_additional_contact = models.CharField(blank=True, null=True, max_length=15)
    email = models.CharField(blank=True, null=True, max_length=200)

    registration_certificates = models.FileField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    gst_registration_number = models.CharField(blank=True, null=True, max_length=150)

    date_of_establishment = models.DateField(blank=True,null=True)

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.pid}"


class PharmacyUsers(models.Model):
    USERS = (
        ('owner', 'owner'),
        ('pharmacist', 'pharmacist'),
    )

    pharmacy_user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

    pharmacy = models.ForeignKey(Pharmacy,on_delete=models.CASCADE,blank=True,null=True)

    role = models.CharField(blank=True, null=True, choices=USERS, max_length=200)

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.pharmacy_user_id}"
