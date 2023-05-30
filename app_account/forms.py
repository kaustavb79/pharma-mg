from django import forms

from app_account.models import ROLES

BUI_LOGIN_ROLES = (
    ('admin', 'ADMIN'),
    ('doctor', 'DOCTOR'),
    ('pharmacist', 'PHARMACIST'),
    ('receptionist', 'RECIPTIONIST'),
)


class BuiLoginForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Username',
                'help_text': 'Enter Username',
                'id': 'floatingInput'
            }
        )
    )
    password = forms.CharField(
        max_length=16,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Password',
                'help_text': 'Enter Password',
                'id': 'floatingPassword'
            }
        ))
    role = forms.ChoiceField(
        choices=BUI_LOGIN_ROLES,
        label="Role",
        initial='',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'id': 'formSelectRole'
            }
        ),
        required=True
    )
