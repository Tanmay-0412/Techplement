import re
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

#register Form
#---------------------------------------------------------------------------------------
class RegisterForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']

     # Custom validation for passwords
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    # Custom validation for email uniqueness
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use. Please use a different email.")
        return email

    # Custom validation for first name (optional)
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match("^[A-Za-z]+$", first_name):
            raise ValidationError("First name should only contain letters.")
        if len(first_name) > 10:
            raise ValidationError(" First Name should be less than 10 caharcters")
        if not first_name:
            raise ValidationError("First name is required.")
        return first_name

    # Custom validation for last name (optional)
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match("^[A-Za-z]+$", last_name):
            raise ValidationError("Last name should only contain letters.")
        if len(last_name) > 10:
            raise ValidationError(" Last Name should be less than 10 caharcters")
        if not last_name:
            raise ValidationError("Last name is required.")
        return last_name