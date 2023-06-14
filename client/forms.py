from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm





class Login_Form(forms.ModelForm):
    username = forms.CharField(label = 'Username' )
    password = forms.CharField(label = 'Password' , widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username' , 'password')