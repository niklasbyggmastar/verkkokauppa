from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    #username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text="")
    last_name = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
