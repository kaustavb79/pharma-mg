from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import logging as log_print

from django.template.loader import render_to_string

from app_account.models import Profile
from app_account.src.utils import generate_random_user
from app_pharma_mg.forms import NewPharmacyRegistrationForm
from app_pharma_mg.models import Pharmacy, PharmacyUsers


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

    context_payload = {
        "profile_get_qs": profile_get_qs,
        "pharmacy_get_qs": pharmacy_get_qs
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

    if request.method == "POST":
        profile_get_qs = Profile.objects.get(user=request.user)
        form = NewPharmacyRegistrationForm(request.POST,request.FILES)
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
                role="pharmacist"
            )

            phar_user_create_qs = PharmacyUsers.objects.create(
                user=profile_create_qs,
                pharmacy=pharmacy_create_qs,
                role="owner",
            )

            return redirect('pharmamg:manage_pharmacy')
    else:
        form = NewPharmacyRegistrationForm()

    context_payload = {"form": form}
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
            pharmacy_get_qs.store_additional_contact = request.POST.get('store_additional_contact', pharmacy_get_qs.store_additional_contact)
            pharmacy_get_qs.email = request.POST.get('store_additional_contact', pharmacy_get_qs.email)
            pharmacy_get_qs.registration_certificates = request.FILES.get('registration_certificates', pharmacy_get_qs.registration_certificates)
            pharmacy_get_qs.registration_certificates = request.POST.get('is_verified', pharmacy_get_qs.is_verified)
            pharmacy_get_qs.is_phone_verified = request.POST.get('is_phone_verified', pharmacy_get_qs.is_phone_verified)
            pharmacy_get_qs.gst_registration_number = request.POST.get('gst_registration_number', pharmacy_get_qs.gst_registration_number)
            pharmacy_get_qs.date_of_establishment = request.POST.get('date_of_establishment', pharmacy_get_qs.date_of_establishment)
            pharmacy_get_qs.save()
            status="success"
            message="Pharmacy Record Updated"

    context_payload = {
        "status": status,
        "message": message,
    }
    return JsonResponse(context_payload)


"""     CLINICS      """


"""
###############################################
            ADMIN VIEWS
        --------------------
                END
###############################################
"""
