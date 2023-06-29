from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Client_Profile

#client_signup
class ClientSignupForm(UserCreationForm):
    username = forms.CharField(label= 'اسم المستخدم')
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='الايميل')
    password1 = forms.CharField(label='كلمه المرور' , widget=forms.PasswordInput(),min_length=8)
    password2 = forms.CharField(label='تاكيد كلمه المرور' , widget=forms.PasswordInput(),min_length=8)
    
    class Meta:
        model = User
        fields = ('username' , 'first_name' , 'last_name' , 'email' , 'password1' , 'password2')

#client_login
class Login_Form(forms.ModelForm):
    username = forms.CharField(label = 'اسم المستخدم' )
    password = forms.CharField(label = 'كلمه المرور' , widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username' , 'password')
        
        
        
        
#update_clienr_profile
class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='الايميل')
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']
        
        
class ClienProfileForm(forms.ModelForm):
    class Meta:
        model = Client_Profile
        exclude = ['user' , 'name']  