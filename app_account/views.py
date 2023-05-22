from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import logging as log_print

from app_account.forms import BuiLoginForm
from app_account.models import Profile


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

                if is_created:
                    messages.success(request, f'Welcome {username.title()}!!!')
                else:
                    messages.success(request, f'Hi {username.title()}, welcome back!')

                return redirect('pharmamg:dashboard')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
    else:
        if request.user.is_authenticated:
            return redirect('pharmamg:dashboard')
        form = BuiLoginForm()

    context_payload = {"form": form}
    return render(request=request, template_name=template, context=context_payload)


@login_required
def business_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("bui_login")