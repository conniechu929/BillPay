from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError
from django import views
from .models import User
import bcrypt
import re


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(max_length=100, label="Confirm password", required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        phone_number = self.cleaned_data['phone_number']
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        PHONE_REGEX = re.compile(r'^\+?1?\d{9,15}$')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match.")
            return confirm_password

        if email and User.objects.filter(email=email).exclude(first_name=first_name, last_name=last_name, phone_number=phone_number).count():
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
            return email

        return self.cleaned_data


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name'].title()
        user.last_name = self.cleaned_data['last_name'].title()
        user.phone_number = self.cleaned_data['phone_number']
        user.email = self.cleaned_data['email']

        unhashed_passwd = self.cleaned_data['password'].encode()
        hashed = bcrypt.hashpw(unhashed_passwd, bcrypt.gensalt())

        user.password = hashed
        if commit:
            user.save()
        return (True, user)

class LogForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']
        exclude = ['first_name', 'last_name', 'phone_number']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']

        try:
            user = User.objects.get(email=email)
        except:
            raise ValidationError("Login fields are invalid.")
            return (False, email)

        if User.objects.get(email=email):
            hashed = bcrypt.hashpw((password).encode(), User.objects.get(email=email).password.encode())
            print "HASHED PW:", hashed
            if User.objects.get(email=email).password == hashed:
                print "CHECKING HASHED PW WITH EMAIL"
                info = User.objects.get(email=email)
                print "INFO RETURNED:", info
                print "EMAIL RETURNED:", info.email
                print "EMAIL RETURNED:", info.id
                # return info
            else:
                raise ValidationError('Password does not match.')
        else:
            raise ValidationError('Email does not exist.')

        return self.cleaned_data

    def find(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']
        hashed = bcrypt.hashpw((password).encode(), User.objects.get(email=email).password.encode())
        if User.objects.get(email=self.cleaned_data.get('email')):
            info = User.objects.get(email=email)
            return (True, info)


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=45, widget=TextInput(attrs={'class': 'form-control','placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=45, widget=TextInput(attrs={'class': 'form-control','placeholder': 'Enter last name'}))
    email = forms.EmailField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Enter email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter password'}))
    confirm_password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm password'}))
    phone_number = forms.CharField(max_length=15, widget=TextInput(attrs={'class': 'form-control','placeholder': 'Enter phone number'}))

class LoginForm(forms.Form):
    email = forms.EmailField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Enter email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter password'}))
