from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput, TextInput, NumberInput, FileInput, CheckboxInput, \
    EmailInput
from django.utils.translation import gettext_lazy as _
from django import forms
from app_pharma_mg.models import Pharmacy, Clinic, Item, Order, Consultation


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

            visible.label_classes = ('col-sm-2', 'col-form-label', 'control-label',)

    def clean(self):
        cleaned_data = super(NewPharmacyRegistrationForm, self).clean()
        email = self.cleaned_data.get("email")
        store_phone = self.cleaned_data.get("store_phone")

        pharmacy_get_qs = self.pharmacy_get_qs
        if pharmacy_get_qs:
            for pharmacy in pharmacy_get_qs:
                if pharmacy.email == email or pharmacy.store_phone == store_phone:
                    raise ValidationError(_('Pharmacy already exists with this email/ phone number!'))


class NewClinicRegistrationForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Clinic
        fields = [
            'name',
            'email',
            'registered_phone',
            'additional_contact',
            'address',
            'registration_certificates',
            'is_verified',
            'is_phone_verified',
            'gst_registration_number',
            'type_of_clinic',
            'date_of_establishment',
            'clinic_timing',
        ]
        widgets = {
            'name': TextInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter Clinic Name',
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
            'registered_phone': NumberInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter clinic associated contact number'
                }
            ),
            'additional_contact': NumberInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter additional contact number'
                }
            ),
            'registration_certificates': FileInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Upload Clinic related registration certificates',
                    'multiple': True
                }
            ),
            'is_verified': CheckboxInput(
                attrs={
                    'class': "form-check-input",
                    'help_text': 'Is Clinic genuine?'
                }
            ),
            'clinic_timing':forms.Select(
                attrs={
                    'class': 'form-select',
                    'id': 'formSelectTiming'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        clinic_get_qs = Clinic.objects.all()
        self.clinic_get_qs = clinic_get_qs

        print('kwargs----0', kwargs)
        print('self.clinic_get_qs----0', self.clinic_get_qs)

        super(NewClinicRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
        self.fields['registered_phone'].label = 'Phone Number'
        self.fields['additional_contact'].label = 'Additional Phone Number'
        self.fields['name'].label = 'Clinic Name'
        self.fields['address'].label = 'Address'

        self.fields['name'].required = True
        self.fields['registered_phone'].required = True
        self.fields['address'].required = True
        self.fields['email'].required = True
        self.fields['gst_registration_number'].required = True
        self.fields['is_verified'].required = True
        self.fields['is_phone_verified'].required = True
        self.fields['date_of_establishment'].required = True
        self.fields['clinic_timing'].required = True

        for visible in self.visible_fields():
            if isinstance(visible.field.widget, CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

            visible.label_classes = ('col-sm-2', 'col-form-label', 'control-label',)

    def clean(self):
        cleaned_data = super(NewClinicRegistrationForm, self).clean()
        email = self.cleaned_data.get("email")
        registered_phone = self.cleaned_data.get("registered_phone")

        clinic_get_qs = self.clinic_get_qs
        if clinic_get_qs:
            for clinic in clinic_get_qs:
                if clinic.email == email or clinic.registered_phone == registered_phone:
                    raise ValidationError(_('Clinic already exists with this email/ phone number!'))


class NewPharmacyEmployeeForm(forms.Form):
    USERS = (
        ('pharmacist', 'Pharmacist'),
    )

    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'First Name',
                'help_text': 'Enter First Name',
                'id': 'floatingInput'
            }
        ),
        required=True
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Last Name',
                'help_text': 'Enter Last Name',
                'id': 'floatingPassword'
            }
        ),
        required=True
    )
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.NumberInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Phone Number',
                'help_text': 'Enter Phone Number',
                'id': 'floatingMobile'
            }
        ),
        required=True
    )
    email = forms.EmailField(
        max_length=100,
        min_length=12,
        widget=forms.EmailInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Email ID',
                'help_text': 'Enter Email ID',
                'id': 'floatingEmail'
            }
        ),
        required=True
    )
    role = forms.ChoiceField(
        choices=USERS,
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

    profile_pic = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'id': 'fileInput',
            }
        )
    )


class AddProductForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Item
        fields = [
            'item_name',
            'item_category',
            'item_price',
            'item_stock',
            'item_composition',
            'item_dose',
            'item_uses',
            'item_image',
            'is_prescription_required',
            'item_side_effects',
            'item_brand',
            'item_manufacturer',
            'item_information',
        ]
        widgets = {
            'item_stock': NumberInput(
                attrs={
                    'class': "form-control",
                    'help_text': 'Enter Product Name',
                }
            ),
            'is_prescription_required': CheckboxInput(
                attrs={
                    'class': "form-check-input",
                    'help_text': 'Is Prescription required?'
                }
            )

        }

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['item_name'].label = 'Product Name'
        self.fields['item_category'].label = 'Product Category'
        self.fields['item_price'].label = 'Price'
        self.fields['item_stock'].label = 'Stock'
        self.fields['item_composition'].label = 'Composition'
        self.fields['item_dose'].label = 'Dose'
        self.fields['item_uses'].label = 'Usage'
        self.fields['item_image'].label = 'Product Image'
        self.fields['is_prescription_required'].label = 'Prescription Required'
        self.fields['item_side_effects'].label = 'Side Effects(if Any)'
        self.fields['item_information'].label = 'Information'
        self.fields['item_brand'].label = 'Brand'
        self.fields['item_manufacturer'].label = 'Manufacturer'

        self.fields['item_name'].required = True
        self.fields['item_category'].required = True
        self.fields['item_price'].required = True
        self.fields['item_stock'].required = True
        self.fields['item_composition'].required = True
        self.fields['item_uses'].required = True
        self.fields['item_image'].required = True
        self.fields['item_manufacturer'].required = True

        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-select'
            if isinstance(visible.field.widget, CheckboxInput):
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

            visible.label_classes = ('col-sm-2', 'col-form-label', 'control-label',)


class NewClinicEmployeeForm(forms.Form):
    USERS = (
        ('doctor', 'DOCTOR'),
        ('reciptionist', 'RECIPTIONIST'),
    )

    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'First Name',
                'help_text': 'Enter First Name',
                'id': 'floatingInput'
            }
        ),
        required=True
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Last Name',
                'help_text': 'Enter Last Name',
                'id': 'floatingPassword'
            }
        ),
        required=True
    )
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.NumberInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Phone Number',
                'help_text': 'Enter Phone Number',
                'id': 'floatingMobile'
            }
        ),
        required=True
    )
    email = forms.EmailField(
        max_length=100,
        min_length=12,
        widget=forms.EmailInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Email ID',
                'help_text': 'Enter Email ID',
                'id': 'floatingEmail'
            }
        ),
        required=True
    )
    role = forms.ChoiceField(
        choices=USERS,
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
    specialization = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Specialization',
                'help_text': 'Enter Specialization',
                'id': 'floatingInputSpecialization'
            }
        )
    )

    profile_pic = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'id': 'fileInput',
            }
        )
    )

