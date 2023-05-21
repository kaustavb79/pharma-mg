from django import forms


class BuiLoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
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
