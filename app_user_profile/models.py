from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError
from django.db.models import JSONField

ROLE_CHOICE = (
    ('admin','ADMIN'),
    ('doctor','DOCTOR'),
    ('nurse','NURSE'),
    ('reciptionist','RECIPTIONIST'),
    ('reciptionist','RECIPTIONIST'),
    ('patient','PATIENT'),
)

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 10.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='profile_picture', validators=[validate_image], null=True, blank=True,
                                       help_text='Maximum file size allowed is 10Mb')
    role = models.CharField(max_length=50, choices=ROLE_CHOICE, null=True, blank=True)

    # contact_number = PhoneNumberField(null=True, blank=True)
    # gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    # blood_group = models.CharField(max_length=20, choices=BLOOD_GROUP_CHOICE, null=True, blank=True)
    # address = models.TextField(null=True, blank=True)
    # city = models.CharField(max_length=100, null=True, blank=True)
    # state = models.CharField(max_length=100, null=True, blank=True)
    # country = models.CharField(max_length=100, null=True, blank=True)
    # postal_code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-created_at',)
        db_table = "%s_%s" % (__package__, "Profile")

    def __str__(self):
        return self.user.username


