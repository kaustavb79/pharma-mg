import uuid

from django.db import models

from app_account.models import Profile

TIMINGS = (
    ('9-6', (
        ('9-10', '9 am to 10 am'),
        ('10-11', '10 am to 11 am'),
        ('11-12', '11 am to 12 pm'),
        ('12-13', '12 pm to 1 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('15-16', '3 pm to 4 pm'),
        ('16-17', '4 pm to 5 pm'),
    )),
    ('9-8', (
        ('9-10', '9 am to 10 am'),
        ('10-11', '10 am to 11 am'),
        ('11-12', '11 am to 12 pm'),
        ('12-13', '12 pm to 1 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('15-16', '3 pm to 4 pm'),
        ('16-17', '4 pm to 5 pm'),
        ('17-18', '5 pm to 6 pm'),
    )),
    ('12-8', (
        ('12-13', '12 pm to 1 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('15-16', '3 pm to 4 pm'),
        ('16-17', '4 pm to 5 pm'),
        ('17-18', '5 pm to 6 pm'),
    )),
    ('12-10', (
        ('12-13', '12 pm to 1 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('14-15', '2 pm to 3 pm'),
        ('15-16', '3 pm to 4 pm'),
        ('16-17', '4 pm to 5 pm'),
        ('17-18', '5 pm to 6 pm'),
        ('18-19', '6 pm to 7 pm'),
        ('19-20', '7 pm to 8 pm'),
        ('20-21', '8 pm to 9 pm'),
    )),
)


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

    date_of_establishment = models.DateField(blank=True, null=True)

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.pid}"


class PharmacyUsers(models.Model):
    USERS = (
        ('owner', 'Store Owner'),
        ('pharmacist', 'Pharmacist'),
    )

    pharmacy_user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, blank=True, null=True)

    role = models.CharField(blank=True, null=True, choices=USERS, max_length=200)

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.pharmacy_user_id}"


class Clinic(models.Model):
    TIMINGS = (
        ('9-6', '9 am to 6 pm'),
        ('9-8', '9 am to 8 pm'),
        ('12-8', '12 am to 8 pm'),
        ('12-10', '12 am to 10 pm'),
    )

    cid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    added_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    name = models.CharField(blank=True, null=True, max_length=200)
    address = models.TextField(blank=True, null=True)

    type_of_clinic = models.CharField(blank=True, null=True, max_length=100)
    clinic_timing = models.CharField(blank=True, null=True, max_length=100, choices=TIMINGS)

    registered_phone = models.CharField(blank=True, null=True, max_length=15)
    additional_contact = models.CharField(blank=True, null=True, max_length=15)
    email = models.CharField(blank=True, null=True, max_length=200)

    registration_certificates = models.FileField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    gst_registration_number = models.CharField(blank=True, null=True, max_length=150)

    date_of_establishment = models.DateField(blank=True, null=True)

    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.cid}"


class ClinicUsers(models.Model):
    USERS = (
        ('doctor', 'Doctor'),
        ('reciptionist', 'Reciptionist'),
    )

    clinic_user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, null=True)
    specialization = models.CharField(blank=True, null=True, max_length=200)

    role = models.CharField(blank=True, null=True, choices=USERS, max_length=200)

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return f"{self.clinic_user_id}"


def product_id_create():
    return "PR_"+uuid.uuid4()

class Item(models.Model):
    CATEGORY = (
        ('drugs', 'DRUG'),
        ('antibiotic', 'ANIT-BIOTICS'),
        ('syrup', 'SYRUP'),
        ('allopathy', 'ALLOPATHY'),
        ('homeopathy', 'HOMEOPATHY'),
        ('vitamins_supplements', 'VITAMINS and SUPPLEMENTS'),
        ('personal_care', 'PERSONAL CARE'),
        ('protein', 'PROTEIN SUPPLEMENTS'),
    )

    item_id = models.CharField(primary_key=True, default=product_id_create,max_length=200)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, blank=True, null=True)

    item_name = models.CharField(blank=True, null=True, max_length=200)
    item_category = models.CharField(blank=True, null=True, choices=CATEGORY, max_length=200)
    item_price = models.FloatField(blank=True, null=True)
    item_stock = models.IntegerField(blank=True, null=True)
    item_composition = models.CharField(blank=True, null=True, max_length=200)
    item_dose = models.CharField(blank=True, null=True, max_length=200)
    item_uses = models.TextField(blank=True, null=True)
    item_side_effects = models.TextField(blank=True, null=True)

    item_brand = models.CharField(blank=True, null=True, max_length=200)
    item_manufacturer = models.CharField(blank=True, null=True, max_length=200)
    item_information = models.TextField(blank=True, null=True)

    item_image = models.FileField(blank=True, null=True)

    is_prescription_required = models.BooleanField(default=False)

    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time', '-updated_on')

    def __str__(self):
        return f"{self.item_name}"


class Prescription(models.Model):
    prescription_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    added_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    prescription_name = models.CharField(blank=True, null=True, max_length=200)
    prescribed_by = models.CharField(blank=True, null=True, max_length=200)

    prescription = models.FileField(blank=True, null=True)

    order_updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time', '-order_updated_on')

    def __str__(self):
        return f"{self.prescription_name}"


class Transaction(models.Model):
    STATUS = (
        ('success', 'SUCCESS'),
        ('incomplete', 'ON HOLD'),
        ('failed', 'FAILED'),
        ('rollbacked', 'ROLLBACKED'),
    )

    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    transaction_status = models.CharField(blank=True, null=True, choices=STATUS, max_length=50)
    transaction_mode = models.CharField(blank=True, null=True, max_length=50)

    order_updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time', '-order_updated_on')

    def __str__(self):
        return f"{self.transaction_id}"


class Order(models.Model):
    MODE = (
        ('online', 'ONLINE'),
        ('offline', 'STORE POS'),
        ('oncall', 'ON CALL ORDER'),
    )

    STATUS = (
        ('placed', 'ORDER PLACED'),
        ('packed', 'ORDER PACKED'),
        ('delivery', 'OUT FOR DELIVERY'),
        ('delivered', 'DELIVERED'),
    )

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    placed_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ManyToManyField(Item, blank=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, blank=True, null=True)

    prescription = models.ManyToManyField(Prescription, blank=True)

    total_amount = models.FloatField(blank=True, null=True)

    mode = models.CharField(blank=True, null=True, choices=MODE, default="offline", max_length=100)
    order_status = models.CharField(blank=True, null=True, choices=STATUS, max_length=100)


    order_updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time', '-order_updated_on')

    def __str__(self):
        return f"{self.order_id}"


class Consultation(models.Model):
    MODE = (
        ('online', 'ONLINE'),
        ('offline', 'CLINIC VISIT'),
        ('oncall', 'ON CALL'),
    )

    STATUS = (
        ('canceled', 'CANCELED'),
        ('rescheduled', 'RESCHUDLED'),
        ('booked', 'BOOKED'),
        ('ongoing', 'ONGOING'),
        ('completed', 'COMPLETED'),
    )

    consultation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    placed_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, null=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, blank=True, null=True)

    total_amount = models.FloatField(blank=True, null=True)

    prescription = models.OneToOneField(Prescription, on_delete=models.CASCADE, blank=True, null=True)

    mode = models.CharField(blank=True, null=True, choices=MODE, default="offline", max_length=100)

    appointment_time = models.CharField(blank=True, null=True, choices=TIMINGS, max_length=100)
    appointment_date = models.CharField(blank=True, null=True, max_length=100)

    status = models.CharField(blank=True, null=True, choices=STATUS, max_length=100)

    order_updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time', '-order_updated_on')

    def __str__(self):
        return f"{self.consultation_id}"
