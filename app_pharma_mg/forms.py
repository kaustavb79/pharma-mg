from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, TextInput, NumberInput, FileInput, CheckboxInput, \
    EmailInput
from django.utils.translation import gettext_lazy as _

from app_pharma_mg.models import Pharmacy


class NewPharmacyRegistrationForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Pharmacy
        fields = [
            'name',
            'email',
            'store_phone',
            'store_additional_contact',
            'address',
            'registration_certificates',
            'is_verified',
            'is_phone_verified',
            'gst_registration_number',
            'date_of_establishment',
        ]
        widgets = {
            'name': TextInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter Pharmacy Name',
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter registered Email ID'
                }
            ),
            'gst_registration_number': TextInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter GST Registration number'
                }
            ),
            'date_of_establishment': DateInput(
                format='%d/%m/%Y',
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter Date Of Establishment',
                    'type': 'date'
                }
            ),
            'store_phone': NumberInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter pharmacy store associated contact number'
                }
            ),
            'store_additional_contact': NumberInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter additional contact number'
                }
            ),
            'registration_certificates': FileInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Upload Pharmacy related registration certificates',
                    'multiple': True
                }
            ),
            'is_verified': CheckboxInput(
                attrs={
                    'class': "form-check-input",
                    'help_text': 'Is Pharmacy genuine?'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        pharmacy_get_qs = Pharmacy.objects.all()
        self.pharmacy_get_qs = pharmacy_get_qs

        print('kwargs----0', kwargs)
        print('self.pharmacy_get_qs----0', self.pharmacy_get_qs)

        super(NewPharmacyRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
        self.fields['store_phone'].label = 'Phone Number'
        self.fields['store_additional_contact'].label = 'Additional Phone Number'
        self.fields['name'].label = 'Pharmacy Name'
        self.fields['address'].label = 'Address'

        self.fields['name'].required = True
        self.fields['store_phone'].required = True
        self.fields['address'].required = True
        self.fields['email'].required = True
        self.fields['gst_registration_number'].required = True
        self.fields['is_verified'].required = True
        self.fields['is_phone_verified'].required = True
        self.fields['date_of_establishment'].required = True

        for visible in self.visible_fields():
            if not isinstance(visible.field.widget, CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-control'
            else:
                visible.field.widget.attrs['class'] = 'form-check-input'

            visible.label_classes = ('col-sm-2','col-form-label',)

    def clean(self):
        cleaned_data = super(NewPharmacyRegistrationForm, self).clean()
        email = self.cleaned_data.get("email")
        store_phone = self.cleaned_data.get("store_phone")

        pharmacy_get_qs = self.pharmacy_get_qs
        if pharmacy_get_qs:
            for pharmacy in pharmacy_get_qs:
                if pharmacy.email == email or pharmacy.store_phone == store_phone:
                    raise ValidationError(_('Pharmacy already exists with this email/ phone number!'))
