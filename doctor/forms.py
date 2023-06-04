from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


""" class Signup_Form(UserCreationForm):
    username = forms.CharField(label= 'Username')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password' , widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(label='Password2' , widget=forms.PasswordInput(), min_length=8)
    
    
    class Meta:
        model = User
        fields = ('username' , 'first_name' , 'last_name' , 'email' , 'password1' , 'password2')
 """




class UserCreationForms(UserCreationForm):
    username = forms.CharField(label= 'username')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='lastname')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='password' , widget=forms.PasswordInput(),min_length=8)
    password2 = forms.CharField(label='password2' , widget=forms.PasswordInput(),min_length=8)
    
    class Meta:
        model = User
        fields = ('username' , 'first_name' , 'last_name' , 'email' , 'password1' , 'password2')





class Login_Form(forms.ModelForm):
    username = forms.CharField(label = 'Username' )
    password = forms.CharField(label = 'Password' , widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username' , 'password')
        
        
        

