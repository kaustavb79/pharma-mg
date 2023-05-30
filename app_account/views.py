from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import logging as log_print

from django.urls import reverse

from app_account.forms import BuiLoginForm
from app_account.models import Profile, OtpVerify
from app_account.src.twilio_v1 import send_otp


def setup_custom_logger(name):
    formatter = log_print.Formatter(fmt='%(asctime)s - %(process)d - %(levelname)s - %(message)s')
    fh = log_print.FileHandler(settings.LOGS_DIR / 'app_account.out')
    fh.setFormatter(formatter)
    logger = log_print.getLogger(name)
    logger.setLevel(log_print.INFO)
    logger.addHandler(fh)
    return logger


logger = setup_custom_logger("app_account")


def home_view(request):
    template = "app_account/html/home.html"

    if request.user.is_authenticated:
        profile_get_qs = Profile.objects.get(user=request.user)
        print("profile_get_qs: ", profile_get_qs)
        if profile_get_qs.role in ['admin', ]:
            return redirect('pharmamg:dashboard')
        elif profile_get_qs.role in ['pharmacist', 'delivery_person']:
            return redirect('pharmamg:pharmacy_dashboard')
        elif profile_get_qs.role in ['doctor', 'receptionist']:
            return redirect('pharmamg:clinic_dashboard')
        elif profile_get_qs.role in ['patient']:
            return redirect('pharmamg:dashboard')

    context_payload = {}
    return render(request=request, template_name=template, context=context_payload)


def business_login(request):
    template = "app_account/html/bui_login_form.html"
    if request.method == "POST":
        form = BuiLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                profile_get_qs, is_created = Profile.objects.get_or_create(
                    user=user,
                    role=role
                )

                print(profile_get_qs)
                if is_created:
                    messages.success(request, f'Welcome {username.title()}!!!')
                else:
                    messages.success(request, f'Hi {username.title()}, welcome back!')

                if profile_get_qs.role in ['admin', ]:
                    return redirect('pharmamg:dashboard')
                elif profile_get_qs.role in ['pharmacist', 'delivery_person']:
                    return redirect('pharmamg:pharmacy_dashboard')
                elif profile_get_qs.role in ['doctor', 'receptionist']:
                    return redirect('pharmamg:clinic_dashboard')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
    else:
        if request.user.is_authenticated:
            profile_get_qs = Profile.objects.get(user=request.user)
            print("profile_get_qs: ", profile_get_qs)
            if profile_get_qs.role in ['admin', ]:
                return redirect('pharmamg:dashboard')
            elif profile_get_qs.role in ['pharmacist', 'delivery_person']:
                return redirect('pharmamg:pharmacy_dashboard')
            elif profile_get_qs.role in ['doctor', 'receptionist']:
                return redirect('pharmamg:dashboard')

        form = BuiLoginForm()

    context_payload = {"form": form}
    return render(request=request, template_name=template, context=context_payload)


@login_required
def business_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("bui_login")





@login_required
def register_user_ajax(request):
    print('request.api_url---', request.api_url)
    status = "failure"
    message = "Invalid Form Data"
    json_response = {}

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        registration_id = request.POST['registration_id']
        hospital_or_clinic_name = request.POST['hospital_or_clinic_name']

        profile_get_qs = get_object_or_404(Profile, user=request.user)
        if profile_get_qs:
            status = "success"
            profile_get_qs.first_name = fname
            profile_get_qs.last_name = lname
            profile_get_qs.phone = phone
            profile_get_qs.email = email
            profile_get_qs.registration_number = registration_id
            profile_get_qs.hospital_clinic_name = hospital_or_clinic_name
            profile_get_qs.save()
            sms_response = send_otp(mobile=phone)

            otp_create_qs = OtpVerify.objects.create(
                otp_sid=sms_response['sid'],
                status=sms_response['status'],
                otp=sms_response['otp'],
                user=profile_get_qs
            )
            message = "Data Saved"
        else:
            message = "Record Not Found"
    else:
        message = "Invalid Request!!!"

    json_response['status'] = status
    json_response['message'] = message

    return JsonResponse(json_response)


@login_required
def verify_mobile_ajax(request):
    template_name = "app_cerviscreen/html/register.html"
    print('request.api_url---', request.api_url)
    status = "failure"
    message = "Invalid Form Data"
    json_response = {}

    if request.method == "POST":
        otp = request.POST['otp']

        profile_get_qs = get_object_or_404(Profile, user=request.user)
        otp_get_qs = OtpVerify.objects.filter(user=profile_get_qs, is_verified=False, has_expired=False).order_by(
            '-date_time')
        print("otp_get_qs: ", otp_get_qs)

        if otp_get_qs:
            if otp_get_qs[0].otp == otp:
                status = "success"
                otp_get_qs[0].is_verified = True
                otp_get_qs[0].has_expired = True
                otp_get_qs[0].save()

                profile_get_qs.is_mobile_verified = True
                profile_get_qs.save()
                message = "Mobile Verified"
                return redirect(reverse("pharmamg_cust:home", kwargs={"role": profile_get_qs.role}))
            else:
                message = "Invalid OTP!!!"
        else:
            message = "Record Not Found"
    else:
        message = "Invalid Request!!!"

    json_response['status'] = status
    json_response['message'] = message

    return render(request, template_name, json_response)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")