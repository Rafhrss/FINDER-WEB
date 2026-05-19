from django import forms

from apps.users.validators import validate_campus_email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email kampus")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean_email(self):
        return validate_campus_email(self.cleaned_data["email"])
