from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Client_Profile

class ClientSignupForm(UserCreationForm):
    username = forms.CharField(label='اسم المستخدم')
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='الايميل')
    password1 = forms.CharField(
        label='كلمه المرور',
        widget=forms.PasswordInput(),
        min_length=8,
        help_text="كلمة المرور يجب أن تحتوي على 8 أحرف على الأقل."
    )
    password2 = forms.CharField(
        label='تاكيد كلمه المرور',
        widget=forms.PasswordInput(),
        min_length=8
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class Login_Form(forms.Form):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(label='كلمه المرور', widget=forms.PasswordInput())

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم الاول')
    last_name = forms.CharField(label='الاسم الاخير')
    email = forms.EmailField(label='الايميل')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client_Profile
        exclude = ['user', 'name']
        labels = {
            'image': 'الصورة الشخصية',
            'address': 'العنوان',
            'address_detail': 'تفاصيل العنوان',
            'number_phone': 'رقم الهاتف',
            'gender': 'الجنس',
            'blood_group': 'فصيلة الدم',
            'date_of_birth': 'تاريخ الميلاد',
            'zip_code': 'الرمز البريدي',
        }