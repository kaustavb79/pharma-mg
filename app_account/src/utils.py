from django.conf import settings
from django.contrib.auth.models import User

from app_account.src.pwd_gen import gen_pwd


def generate_random_user(user_name, first_name, last_name, email, phone):
    # create user
    new_user = User.objects.create(
        username=user_name,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    new_user.is_active = True
    new_user.set_password(gen_pwd())
    new_user.save()
    return new_user


def generate_random_patient_user(user_name, first_name, last_name, email):
    # create user
    new_user = User.objects.create(
        username=user_name,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    password = settings.CUSTOMER_LOGIN_PWD
    new_user.is_active = True
    new_user.set_password(password)
    new_user.save()
    return new_user