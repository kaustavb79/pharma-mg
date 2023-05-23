from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import logging as log_print

from app_account.models import Profile
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
        form = NewPharmacyRegistrationForm(request.POST, {"profile_get_qs": profile_get_qs})
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            print(form_cleaned_data)
            return redirect('pharmamg:manage_pharmacy')
    else:
        form = NewPharmacyRegistrationForm()

    context_payload = {"form": form}
    return render(request=request, template_name=template, context=context_payload)
