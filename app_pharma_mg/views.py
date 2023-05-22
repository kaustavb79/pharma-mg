from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import logging as log_print

from app_account.models import Profile


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
    template = "app_pharma_mg/html/dashboard.html"

    profile_get_qs = get_object_or_404(Profile,user=request.user)

    context_payload = {
        "profile_get_qs":profile_get_qs
    }
    return render(request=request, template_name=template, context=context_payload)
