from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile_Doctor , Doctor_Image


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



#doctor_signup
class SignupForm(UserCreationForm):
    username = forms.CharField(label= 'اسم المستخدم')
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='الايميل')
    password1 = forms.CharField(label='كلمه المرور' , widget=forms.PasswordInput(),min_length=8)
    password2 = forms.CharField(label='تاكيد كلمه المرور' , widget=forms.PasswordInput(),min_length=8)
    class Meta:
        model = User
        fields = ('username' , 'first_name' , 'last_name' , 'email' , 'password1' , 'password2')



class Complate_DocDate_Form(forms.ModelForm):
    class Meta:
        model = Profile_Doctor
        fields = ['name' , 'number_phone', 'specialization' ,'Syndicate']  


#doctor_login
class Login_Form(forms.ModelForm):
    username = forms.CharField(label = 'اسم المستخدم' )
    password = forms.CharField(label = 'كلمه المرور' , widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username' , 'password')
        
        
        
        
#update_doctor_profile
class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='الايميل')
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']
        
        
class ProfileDoctorForm(forms.ModelForm):
    
    class Meta:
        model = Profile_Doctor
        exclude = ['user' , 'active_doctor' , 'Syndicate' , 'google_link' , 'tags' ,'who_i' , 'specialization']        
        
        
""" class Doctor_Image_form(forms.ModelForm):
    class Meta:
        model = Doctor_Image
        exclude = ['doctor']  """       
    
