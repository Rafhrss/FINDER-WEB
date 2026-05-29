from django import forms

from apps.users.models import User
from apps.users.validators import validate_campus_email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email kampus")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean_email(self):
        return validate_campus_email(self.cleaned_data["email"])


class RegisterForm(forms.Form):
    name = forms.CharField(label="Nama", max_length=120)
    email = forms.EmailField(label="Email kampus")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        min_length=8,
    )
    password2 = forms.CharField(
        label="Konfirmasi password",
        widget=forms.PasswordInput,
        min_length=8,
    )

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_email(self):
        email = validate_campus_email(self.cleaned_data["email"])
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email ini sudah terdaftar.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Konfirmasi password tidak sama.")
        return cleaned_data
