from django.forms import ModelForm, BooleanField, DateInput, TextInput, NumberInput, FileInput

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
        }

    def __init__(self, *args, **kwargs):
        profile_get_qs = kwargs.get("profile_get_qs", False)
        self.profile_get_qs = profile_get_qs

        print('kwargs----0', kwargs)

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
        self.fields['email'].required = True
        self.fields['gst_registration_number'].required = True

        self.fields['is_verified'] = BooleanField(initial=False, required=False)
        self.fields['is_phone_verified'] = BooleanField(initial=False, required=False)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(NewPharmacyRegistrationForm, self).clean()
        email = self.cleaned_data.get("email")