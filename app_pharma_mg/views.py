import logging as log_print
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from app_account.models import Profile
from app_account.src.utils import generate_random_user, generate_random_patient_user
from app_pharma_mg.forms import NewPharmacyRegistrationForm, NewPharmacyEmployeeForm, NewClinicRegistrationForm, \
    AddProductForm, NewClinicEmployeeForm
from app_pharma_mg.models import Pharmacy, PharmacyUsers, Clinic, ClinicUsers, Order, Item, Transaction, Consultation, \
    TIMINGS


def setup_custom_logger(name):
    formatter = log_print.Formatter(fmt='%(asctime)s - %(process)d - %(levelname)s - %(message)s')
    fh = log_print.FileHandler(settings.LOGS_DIR / 'app_pharma_mg.out')
    fh.setFormatter(formatter)
    logger = log_print.getLogger(name)
    logger.setLevel(log_print.INFO)
    logger.addHandler(fh)
    return logger


logger = setup_custom_logger("app_pharma_mg")

"""
###############################################
            ADMIN VIEWS
        --------------------
               START
###############################################
"""


@login_required
def dashboard_view(request):
    template = "app_pharma_mg/bui/html/dashboard.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    pharmacy_get_qs = Pharmacy.objects.all()
    clinic_get_qs = Clinic.objects.all()

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "pharmacy_get_qs": pharmacy_get_qs,
        "clinic_get_qs": clinic_get_qs
    }
    return render(request=request, template_name=template, context=context_payload)


"""     PHARMACY      """


@login_required
def manage_pharmacy_view(request):
    template = "app_pharma_mg/bui/html/manage_pharmacy.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    pharmacy_get_qs = Pharmacy.objects.all()
    pharmacy_user_get_qs = PharmacyUsers.objects.filter(pharmacy__in=pharmacy_get_qs)

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "pharmacy_user_get_qs": pharmacy_user_get_qs
    }
    return render(request=request, template_name=template, context=context_payload)


@login_required
def add_pharmacy(request):
    template = "app_pharma_mg/bui/html/add_pharmacy.html"
    profile_get_qs = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = NewPharmacyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            name = form_cleaned_data['name']
            email = form_cleaned_data['email']
            store_phone = form_cleaned_data['store_phone']
            store_additional_contact = form_cleaned_data['store_additional_contact']
            address = form_cleaned_data['address']
            registration_certificates = form_cleaned_data['registration_certificates']
            is_verified = form_cleaned_data['is_verified']
            is_phone_verified = form_cleaned_data['is_phone_verified']
            gst_registration_number = form_cleaned_data['gst_registration_number']
            date_of_establishment = form_cleaned_data['date_of_establishment']

            pharmacy_create_qs = Pharmacy.objects.create(
                added_by=profile_get_qs,
                name=name,
                email=email,
                store_phone=store_phone,
                store_additional_contact=store_additional_contact,
                address=address,
                registration_certificates=registration_certificates,
                is_verified=is_verified,
                is_phone_verified=is_phone_verified,
                gst_registration_number=gst_registration_number,
                date_of_establishment=date_of_establishment,
            )

            # Owner create for Pharmacy
            username = f"{name.replace(' ', '_').lower()}__{pharmacy_create_qs.pk}__owner"
            owner = generate_random_user(username, first_name=f"Pharmacy_{pharmacy_create_qs.pk}", last_name="Owner",
                                         email=email, phone=store_phone)

            profile_create_qs = Profile.objects.create(
                user=owner,
                role="pharmacist",
                first_name=f"Pharmacy_{pharmacy_create_qs.pk}",
                last_name="Owner",
                email=email,
                phone=store_phone
            )

            phar_user_create_qs = PharmacyUsers.objects.create(
                user=profile_create_qs,
                pharmacy=pharmacy_create_qs,
                role="owner",
            )

            return redirect('pharmamg:manage_pharmacy')
    else:
        form = NewPharmacyRegistrationForm()

    context_payload = {"form": form, "profile_get_qs": profile_get_qs}
    return render(request=request, template_name=template, context=context_payload)


@login_required
def delete_pharmacy_ajax(request, pharmacy_id: str):
    print('request.api_url---', request.api_url)

    try:
        pharmacy_get_qs = get_object_or_404(Pharmacy, pk=pharmacy_id)
    except:
        logger.exception("Delete Pharmacy Exception: ")
    else:
        pharmacy_get_qs.delete()

    return redirect("pharmamg:manage_pharmacy")


@login_required
def edit_form_ajax(request):
    status = "failure"
    message = "Invalid ID"

    if request.method == "POST":
        pharmacy_id = request.POST.get('pharmacy_id')
        try:
            pharmacy_get_qs = Pharmacy.objects.get(pk=pharmacy_id)
        except:
            message = "Invalid Pharmacy ID"
        else:
            pharmacy_get_qs.name = request.POST.get('name', pharmacy_get_qs.name)
            pharmacy_get_qs.address = request.POST.get('address', pharmacy_get_qs.address)
            pharmacy_get_qs.store_phone = request.POST.get('store_phone', pharmacy_get_qs.store_phone)
            pharmacy_get_qs.store_additional_contact = request.POST.get('store_additional_contact',
                                                                        pharmacy_get_qs.store_additional_contact)
            pharmacy_get_qs.email = request.POST.get('store_additional_contact', pharmacy_get_qs.email)
            pharmacy_get_qs.registration_certificates = request.FILES.get('registration_certificates',
                                                                          pharmacy_get_qs.registration_certificates)
            pharmacy_get_qs.registration_certificates = request.POST.get('is_verified', pharmacy_get_qs.is_verified)
            pharmacy_get_qs.is_phone_verified = request.POST.get('is_phone_verified', pharmacy_get_qs.is_phone_verified)
            pharmacy_get_qs.gst_registration_number = request.POST.get('gst_registration_number',
                                                                       pharmacy_get_qs.gst_registration_number)
            pharmacy_get_qs.date_of_establishment = request.POST.get('date_of_establishment',
                                                                     pharmacy_get_qs.date_of_establishment)
            pharmacy_get_qs.save()
            status = "success"
            message = "Pharmacy Record Updated"

    context_payload = {
        "status": status,
        "message": message,
    }
    return JsonResponse(context_payload)


"""     CLINICS      """


@login_required
def manage_clinic_view(request):
    template = "app_pharma_mg/bui/html/manage_clinic.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    clinic_get_qs = Clinic.objects.all()
    clinic_user_get_qs = ClinicUsers.objects.filter(clinic__in=clinic_get_qs)

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "clinic_user_get_qs": clinic_user_get_qs
    }
    return render(request=request, template_name=template, context=context_payload)


@login_required
def add_clinic(request):
    template = "app_pharma_mg/bui/html/add_clinic.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = NewClinicRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            name = form_cleaned_data['name']
            email = form_cleaned_data['email']
            registered_phone = form_cleaned_data['registered_phone']
            additional_contact = form_cleaned_data['additional_contact']
            address = form_cleaned_data['address']
            registration_certificates = form_cleaned_data['registration_certificates']
            is_verified = form_cleaned_data['is_verified']
            is_phone_verified = form_cleaned_data['is_phone_verified']
            gst_registration_number = form_cleaned_data['gst_registration_number']
            type_of_clinic = form_cleaned_data['type_of_clinic']
            date_of_establishment = form_cleaned_data['date_of_establishment']

            clinic_create_qs = Clinic.objects.create(
                added_by=profile_get_qs,
                name=name,
                email=email,
                registered_phone=registered_phone,
                additional_contact=additional_contact,
                address=address,
                registration_certificates=registration_certificates,
                is_verified=is_verified,
                is_phone_verified=is_phone_verified,
                type_of_clinic=type_of_clinic,
                gst_registration_number=gst_registration_number,
                date_of_establishment=date_of_establishment,
            )

            # Owner create for Clinic
            username = f"{name.replace(' ', '_').lower()}__{clinic_create_qs.pk}__owner"
            owner = generate_random_user(username, first_name=f"Clinic_{clinic_create_qs.pk}", last_name="Owner",
                                         email=email, phone=registered_phone)

            profile_create_qs = Profile.objects.create(
                user=owner,
                role="doctor",
                first_name=f"Clinic_{clinic_create_qs.pk}",
                last_name="Owner",
                email=email,
                phone=registered_phone,
            )

            clinic_user_create_qs = ClinicUsers.objects.create(
                user=profile_create_qs,
                clinic=clinic_create_qs,
                role="doctor",
            )

            return redirect('pharmamg:manage_clinic')
    else:
        form = NewClinicRegistrationForm()

    context_payload = {"form": form, "profile_get_qs": profile_get_qs}
    return render(request=request, template_name=template, context=context_payload)


@login_required
def delete_clinic_ajax(request, clinic_id: str):
    print('request.api_url---', request.api_url)

    try:
        clinic_get_qs = get_object_or_404(Clinic, pk=clinic_id)
    except:
        logger.exception("Delete Clinic Exception: ")
    else:
        clinic_get_qs.delete()

    return redirect("pharmamg:manage_clinic")


@login_required
def edit_clinic_form_ajax(request):
    status = "failure"
    message = "Invalid ID"

    if request.method == "POST":
        clinic_id = request.POST.get('clinic_id')
        try:
            clinic_get_qs = Clinic.objects.get(pk=clinic_id)
        except:
            message = "Invalid Clinic ID"
        else:
            clinic_get_qs.name = request.POST.get('name', clinic_get_qs.name)
            clinic_get_qs.address = request.POST.get('address', clinic_get_qs.address)
            clinic_get_qs.type_of_clinic = request.POST.get('type_of_clinic', clinic_get_qs.type_of_clinic)
            clinic_get_qs.registered_phone = request.POST.get('registered_phone', clinic_get_qs.registered_phone)
            clinic_get_qs.additional_contact = request.POST.get('additional_contact', clinic_get_qs.additional_contact)
            clinic_get_qs.email = request.POST.get('store_additional_contact', clinic_get_qs.email)
            clinic_get_qs.registration_certificates = request.FILES.get('registration_certificates',
                                                                        clinic_get_qs.registration_certificates)
            clinic_get_qs.registration_certificates = request.POST.get('is_verified', clinic_get_qs.is_verified)
            clinic_get_qs.is_phone_verified = request.POST.get('is_phone_verified', clinic_get_qs.is_phone_verified)
            clinic_get_qs.gst_registration_number = request.POST.get('gst_registration_number',
                                                                     clinic_get_qs.gst_registration_number)
            clinic_get_qs.date_of_establishment = request.POST.get('date_of_establishment',
                                                                   clinic_get_qs.date_of_establishment)
            clinic_get_qs.save()
            status = "success"
            message = "Clinic Record Updated"

    context_payload = {
        "status": status,
        "message": message,
    }
    return JsonResponse(context_payload)


"""
###############################################
            ADMIN VIEWS
        --------------------
                END
###############################################
"""

"""
###############################################
            PHARMACY VIEWS
        --------------------
                START
###############################################
"""


@login_required
def dashboard_pharmacy_view(request):
    template = "app_pharma_mg/bui/html/pharmacy/dashboard_pharmacy.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs)
    pharmacy_get_qs = pharmacy_user_get_qs.pharmacy
    orders_filter_qs = Order.objects.filter(store=pharmacy_get_qs)
    items_filter_qs = Item.objects.filter(pharmacy=pharmacy_get_qs)
    pharmacy_users_filter_qs = PharmacyUsers.objects.filter(pharmacy=pharmacy_get_qs)

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "pharmacy_get_qs": pharmacy_get_qs,
        "pharmacy_user_get_qs": pharmacy_user_get_qs,
        "orders_filter_qs": orders_filter_qs,
        "items_filter_qs": items_filter_qs,
        "pharmacy_users_filter_qs": pharmacy_users_filter_qs,
    }
    return render(request=request, template_name=template, context=context_payload)


@login_required
def manage_pharmacy_user_view(request):
    template = "app_pharma_mg/bui/html/pharmacy/manage_employee.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs)
    pharmacy_users_filter_qs = PharmacyUsers.objects.none()
    if pharmacy_user_get_qs.role == 'owner':
        pharmacy_users_filter_qs = PharmacyUsers.objects.filter(pharmacy=pharmacy_user_get_qs.pharmacy,
                                                                role="pharmacist")

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "pharmacy_user_get_qs": pharmacy_user_get_qs,
        "pharmacy_users_filter_qs": pharmacy_users_filter_qs,
    }
    return render(request=request, template_name=template, context=context_payload)


@login_required
def add_pharmacy_employee(request):
    template = "app_pharma_mg/bui/html/pharmacy/add_employee.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs, role="owner")
    if request.method == "POST":
        form = NewPharmacyEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            first_name = form_cleaned_data['first_name']
            last_name = form_cleaned_data['last_name']
            phone = form_cleaned_data['phone']
            email = form_cleaned_data['email']
            role = form_cleaned_data['role']
            profile_pic = form_cleaned_data['profile_pic']

            try:
                check_if_user_exists_mail = Profile.objects.get(email=email)
                check_if_user_exists_phone = Profile.objects.get(phone=phone)
            except:
                logger.exception("No Profile Exists")
                # Owner create employee for Pharmacy
                username = f"{first_name.replace(' ', '_').lower()}__{random.randint(1000, 9999)}"
                user = generate_random_user(username, first_name=first_name, last_name=last_name,
                                            email=email, phone=phone)

                profile_create_qs = Profile.objects.create(
                    user=user,
                    role=role,
                    phone=phone,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    profile_pic=profile_pic
                )

                pharmacy_user_create_qs = PharmacyUsers.objects.create(
                    user=profile_create_qs,
                    pharmacy=pharmacy_user_get_qs.pharmacy,
                    role=role,
                )
            else:
                if check_if_user_exists_mail or check_if_user_exists_phone:
                    messages.error("User With Given Email id / Mobile NUmber Already exists")
                else:
                    # Owner create employee for Pharmacy
                    username = f"{first_name.replace(' ', '_').lower()}__{random.randint(1000, 9999)}"
                    user = generate_random_user(username, first_name=first_name, last_name=last_name,
                                                email=email, phone=phone)

                    profile_create_qs = Profile.objects.create(
                        user=user,
                        role=role,
                        phone=phone,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        profile_pic=profile_pic
                    )

                    pharmacy_user_create_qs = PharmacyUsers.objects.create(
                        user=profile_create_qs,
                        pharmacy=pharmacy_user_get_qs.pharmacy,
                        role=role,
                    )
            return redirect('pharmamg:manage_pharmacy_users')
    else:
        form = NewPharmacyEmployeeForm()

    context_payload = {"form": form, "profile_get_qs": profile_get_qs, "pharmacy_user_get_qs": pharmacy_user_get_qs}
    return render(request=request, template_name=template, context=context_payload)


@login_required
def delete_pharmacy_employee_ajax(request, user_id: str):
    print('request.api_url---', request.api_url)

    try:
        pharmacy_user_get_qs = get_object_or_404(PharmacyUsers, pk=user_id)
    except:
        logger.exception("Delete Pharmacy User Exception: ")
    else:
        pharmacy_user_get_qs.delete()

    return redirect("pharmamg:manage_pharmacy_users")


# ITEMS
@login_required
def manage_pharmacy_products_view(request):
    template = "app_pharma_mg/bui/html/pharmacy/manage_product.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs)
    items_filter_qs = Item.objects.filter(pharmacy=pharmacy_user_get_qs.pharmacy)

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "pharmacy_user_get_qs": pharmacy_user_get_qs,
        "items_filter_qs": items_filter_qs
    }
    return render(request=request, template_name=template, context=context_payload)


@login_required
def add_pharmacy_product(request):
    template = "app_pharma_mg/bui/html/pharmacy/add_product.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs)
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            item_name = form_cleaned_data['item_name']
            item_category = form_cleaned_data['item_category']
            item_price = form_cleaned_data['item_price']
            item_stock = form_cleaned_data['item_stock']
            item_composition = form_cleaned_data['item_composition']
            item_uses = form_cleaned_data['item_uses']
            item_dose = form_cleaned_data['item_dose']
            item_side_effects = form_cleaned_data['item_side_effects']
            item_brand = form_cleaned_data['item_brand']
            item_manufacturer = form_cleaned_data['item_manufacturer']
            item_information = form_cleaned_data['item_information']
            item_image = form_cleaned_data['item_image']
            is_prescription_required = form_cleaned_data['is_prescription_required']

            item_create_qs = Item.objects.create(
                item_name=item_name,
                item_category=item_category,
                item_price=item_price,
                item_stock=item_stock,
                item_composition=item_composition,
                item_dose=item_dose,
                item_uses=item_uses,
                item_side_effects=item_side_effects,
                item_brand=item_brand,
                item_manufacturer=item_manufacturer,
                item_information=item_information,
                item_image=item_image,
                is_prescription_required=is_prescription_required,
                pharmacy=pharmacy_user_get_qs.pharmacy,
            )
            messages.success(request, "New Item Created",
                             {"profile_get_qs": profile_get_qs, "pharmacy_user_get_qs": pharmacy_user_get_qs})

            return redirect('pharmamg:manage_pharmacy_products')
    else:
        form = AddProductForm()

    context_payload = {"form": form, "profile_get_qs": profile_get_qs, "pharmacy_user_get_qs": pharmacy_user_get_qs}
    return render(request=request, template_name=template, context=context_payload)


@login_required
def edit_product_form_ajax(request):
    status = "failure"
    message = "Invalid ID"

    if request.method == "POST":
        item_id = request.POST.get('item_id')
        try:
            item_get_qs = Item.objects.get(pk=item_id)
        except:
            message = "Invalid Item ID"
        else:
            item_get_qs.item_image = request.POST.get('item_image', item_get_qs.item_image)
            item_get_qs.item_stock = request.POST.get('item_stock', item_get_qs.item_stock)
            item_get_qs.save()
            status = "success"
            message = "Item Record Updated"

    context_payload = {
        "status": status,
        "message": message,
    }
    return JsonResponse(context_payload)


# ORDERS

@login_required
def manage_pharmacy_orders_view(request):
    template = "app_pharma_mg/bui/html/pharmacy/manage_orders.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs)
    orders_filter_qs = Order.objects.filter(store=pharmacy_user_get_qs.pharmacy)

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "pharmacy_user_get_qs": pharmacy_user_get_qs,
        "orders_filter_qs": orders_filter_qs
    }
    print(context_payload)
    return render(request=request, template_name=template, context=context_payload)


@login_required
def create_order_pharmacy_view(request):
    template = "app_pharma_mg/bui/html/pharmacy/create_order.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs)
    item_filter_qs = Item.objects.filter(pharmacy=pharmacy_user_get_qs.pharmacy)
    context_payload = {"item_filter_qs": item_filter_qs, "profile_get_qs": profile_get_qs,
                       "pharmacy_user_get_qs": pharmacy_user_get_qs}
    return render(request=request, template_name=template, context=context_payload)


def create_order_ajax(request):
    status = "failure"

    if request.method == "POST":
        patient_name = request.POST.get('patient_name', 'Anonymous')
        patient_mobile = request.POST.get('patient_mobile')
        patient_address = request.POST.get('patient_address')
        mode = request.POST.get('mode')
        payment_mode = request.POST.get('payment_mode')
        payment_status = request.POST.get('payment_status')
        items = request.POST.getlist('item[]')

        first_name = "Anonymous"
        last_name = "User"
        if patient_name != "Anonymous":
            first_name = patient_name

        profile_get_qs = Profile.objects.get(user=request.user)
        pharmacy_user_get_qs = PharmacyUsers.objects.get(user=profile_get_qs)

        try:
            patient_profile_get_qs = Profile.objects.get(phone=patient_mobile, role="patient")
        except:

            # Create Patient
            username = f"{first_name.replace(' ', '_').lower()}__{random.randint(1000, 9999)}"
            user = generate_random_patient_user(username, first_name=first_name, last_name=last_name,
                                                email=f"abc{random.randint(1000, 9999)}@gmail.com")
            patient_profile_create_qs = Profile.objects.create(
                user=user,
                role="patient",
                phone=patient_mobile,
                first_name=first_name,
                last_name=last_name,
                user_address=patient_address
            )
            logger.exception("Patient Created")
        patient_profile_get_qs = Profile.objects.get(phone=patient_mobile, role='patient')
        item_filter_qs = Item.objects.filter(pharmacy=pharmacy_user_get_qs.pharmacy)
        print(item_filter_qs)

        total_amount = 0.0
        for item in item_filter_qs:
            total_amount += item.item_price

        transaction_create_qs = Transaction.objects.create(
            transaction_status=payment_status,
            transaction_mode=payment_mode,
        )

        order_create_qs = Order.objects.create(
            placed_by=patient_profile_get_qs,
            store=pharmacy_user_get_qs.pharmacy,
            mode=mode,
            total_amount=total_amount,
            transaction=transaction_create_qs
        )
        for item in item_filter_qs:
            if item.item_id in items:
                order_create_qs.item.add(item)

        status = "success"

    json_response = {"status": status}
    return JsonResponse(json_response)


"""
###############################################
            PHARMACY VIEWS
        --------------------
                END
###############################################
"""

"""
###############################################
            CLINIC VIEWS
        --------------------
                START
###############################################
"""


@login_required
def dashboard_clinic_view(request):
    template = "app_pharma_mg/bui/html/clinic/dashboard_clinic.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)
    clinic_user_get_qs = ClinicUsers.objects.get(user=profile_get_qs)
    clinic_get_qs = clinic_user_get_qs.clinic
    clinic_users_filter_qs = ClinicUsers.objects.filter(clinic=clinic_get_qs)
    consultation_get_qs = Consultation.objects.filter(clinic=clinic_get_qs)

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "clinic_get_qs": clinic_get_qs,
        "clinic_user_get_qs": clinic_user_get_qs,
        "clinic_users_filter_qs": clinic_users_filter_qs,
        "consultation_get_qs": consultation_get_qs,
    }
    return render(request=request, template_name=template, context=context_payload)


@login_required
def manage_clinic_user_view(request):
    template = "app_pharma_mg/bui/html/clinic/manage_employee.html"

    profile_get_qs = get_object_or_404(Profile, user=request.user)

    clinic_user_get_qs = ClinicUsers.objects.get(user=profile_get_qs)
    clinic_get_qs = clinic_user_get_qs.clinic

    clinic_users_filter_qs = PharmacyUsers.objects.none()
    if clinic_user_get_qs.role == 'doctor':
        clinic_users_filter_qs = ClinicUsers.objects.filter(clinic=clinic_get_qs)

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "clinic_user_get_qs": clinic_user_get_qs,
        "clinic_users_filter_qs": clinic_users_filter_qs,
    }
    return render(request=request, template_name=template, context=context_payload)


@login_required
def add_clinic_employee(request):
    template = "app_pharma_mg/bui/html/clinic/add_employee.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    clinic_user_get_qs = ClinicUsers.objects.get(user=profile_get_qs, role="doctor")
    if request.method == "POST":
        form = NewClinicEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            first_name = form_cleaned_data['first_name']
            last_name = form_cleaned_data['last_name']
            phone = form_cleaned_data['phone']
            email = form_cleaned_data['email']
            role = form_cleaned_data['role']
            profile_pic = form_cleaned_data['profile_pic']
            specialization = form_cleaned_data['specialization']

            try:
                check_if_user_exists_mail = Profile.objects.get(email=email)
                check_if_user_exists_phone = Profile.objects.get(phone=phone)
            except:
                logger.exception("No Profile Exists")
                # Owner create employee for Clinic
                username = f"{first_name.replace(' ', '_').lower()}__{random.randint(1000, 9999)}"
                user = generate_random_user(username, first_name=first_name, last_name=last_name,
                                            email=email, phone=phone)

                profile_create_qs = Profile.objects.create(
                    user=user,
                    role=role,
                    phone=phone,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    profile_pic=profile_pic
                )

            profile_create_qs = Profile.objects.get(
                role=role,
                phone=phone,
                email=email,
            )
            clinic_user_create_qs = ClinicUsers.objects.create(
                user=profile_create_qs,
                clinic=clinic_user_get_qs.clinic,
                role=role,
                specialization=specialization,
            )
            messages.success(request, "New Clinic User Added",
                             {"profile_get_qs": profile_get_qs, "clinic_user_get_qs": clinic_user_get_qs})
            return redirect('pharmamg:manage_clinic_users')
    else:
        form = NewClinicEmployeeForm()

    context_payload = {"form": form, "profile_get_qs": profile_get_qs, "clinic_user_get_qs": clinic_user_get_qs}
    return render(request=request, template_name=template, context=context_payload)


@login_required
def delete_clinic_employee_ajax(request, user_id: str):
    print('request.api_url---', request.api_url)

    try:
        clinic_user_get_qs = get_object_or_404(ClinicUsers, pk=user_id)
    except:
        logger.exception("Delete Clinic User Exception: ")
    else:
        clinic_user_get_qs.delete()

    return redirect("pharmamg:manage_clinic_users")


@login_required
def schedule_consultation_view(request):
    template = "app_pharma_mg/bui/html/clinic/create_appointments.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    clinic_user_get_qs = ClinicUsers.objects.get(user=profile_get_qs)
    consultation_filter_qs = Consultation.objects.filter(clinic=clinic_user_get_qs.clinic,
                                                         appointment_time=clinic_user_get_qs.clinic.clinic_timing)
    timing_dict = {}
    for time in dict(TIMINGS)[clinic_user_get_qs.clinic.clinic_timing]:
        timing_dict[time[0]] = time[1]
    context_payload = {"consultation_filter_qs": consultation_filter_qs, "profile_get_qs": profile_get_qs,
                       "clinic_user_get_qs": clinic_user_get_qs, "timings": timing_dict}
    # print(context_payload)
    return render(request=request, template_name=template, context=context_payload)


def schedule_consultation_ajax(request):
    status = "success"
    message = "Failed"

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name', 'Anonymous')
        patient_mobile = request.POST.get('patient_mobile')
        patient_address = request.POST.get('patient_address')
        mode = request.POST.get('mode')
        payment_mode = request.POST.get('payment_mode')
        payment_status = request.POST.get('payment_status')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        consultation_charge = request.POST.get('consultation_charge')

        first_name = "Anonymous"
        last_name = "User"
        if patient_name != "Anonymous":
            first_name = patient_name

        profile_get_qs = Profile.objects.get(user=request.user)
        clinic_user_get_qs = ClinicUsers.objects.get(user=profile_get_qs)

        try:
            patient_profile_get_qs = Profile.objects.get(phone=patient_mobile, role="patient")
        except:

            # Create Patient
            username = f"{first_name.replace(' ', '_').lower()}__{random.randint(1000, 9999)}"
            user = generate_random_patient_user(username, first_name=first_name, last_name=last_name,
                                                email=f"abc{random.randint(1000, 9999)}@gmail.com")
            patient_profile_create_qs = Profile.objects.create(
                user=user,
                role="patient",
                phone=patient_mobile,
                first_name=first_name,
                last_name=last_name,
                user_address=patient_address
            )
            logger.exception("Patient Created")

        patient_profile_get_qs = Profile.objects.get(phone=patient_mobile, role='patient')
        consultation_filter_qs = Consultation.objects.filter(clinic=clinic_user_get_qs.clinic,
                                                             status__in=['booked', 'rescheduled'],
                                                             appointment_date=appointment_date,
                                                             appointment_time=appointment_time)
        print(consultation_filter_qs)

        if not consultation_filter_qs:
            total_amount = consultation_charge

            transaction_create_qs = Transaction.objects.create(
                transaction_status=payment_status,
                transaction_mode=payment_mode,
            )

            order_create_qs = Consultation.objects.create(
                placed_by=patient_profile_get_qs,
                clinic=clinic_user_get_qs.clinic,
                status='booked',
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                mode=mode,
                total_amount=total_amount,
                transaction=transaction_create_qs
            )

            status = "success"
        else:
            message = "Booking Already Exists"

    json_response = {"status": status, "message": message}
    return JsonResponse(json_response)


@login_required
def manage_consultation_view(request):
    template = "app_pharma_mg/bui/html/clinic/manage_appointments.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    clinic_user_get_qs = ClinicUsers.objects.get(user=profile_get_qs)
    consultation_filter_qs = Consultation.objects.filter(clinic=clinic_user_get_qs.clinic)
    timing_dict = {}
    for time in dict(TIMINGS)[clinic_user_get_qs.clinic.clinic_timing]:
        timing_dict[time[0]] = time[1]
    context_payload = {"consultation_filter_qs": consultation_filter_qs, "profile_get_qs": profile_get_qs,
                       "clinic_user_get_qs": clinic_user_get_qs, "timings": timing_dict}
    # print(context_payload)
    return render(request=request, template_name=template, context=context_payload)


"""
###############################################
            CLINIC VIEWS
        --------------------
                END
###############################################
"""

"""
###############################################
            PATIENT VIEWS
        --------------------
                START
###############################################
"""


@login_required
def patient_home(request):
    template = "app_pharma_mg/customer/product_view.html"

    profile_get_qs = Profile.objects.get(user=request.user)
    product_get_qs = Item.objects.all()
    context_payload = {
        "profile_get_qs": profile_get_qs,
        "product_get_qs": product_get_qs
    }
    return render(request=request, template_name=template, context=context_payload)


"""
###############################################
            PATIENT VIEWS
        --------------------
                END
###############################################
"""
