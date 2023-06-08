from django.shortcuts import render , redirect
from django.urls import reverse
from .models import Profile_Doctor
from .forms import Login_Form , UserCreationForms
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages






# Create your views here.

""" def doctors_list2(request):
    doctors = User.objects.all()
    return render(request , 'users/index.html.html' , context={'doctors':doctors,})  """  

def welcome(request):
    return render(request,'doctor/doctors_list.html', context={})

    
def doctors_list(request):
    doctors = User.objects.all()
    return render(request , 'doctor/doctors_list.html' , context={'doctors':doctors,})


def doctors_detail(request , slug):
    doctors_detail = Profile_Doctor.objects.get(slug = slug)
    return render(request , 'doctor/doctor-profile.html' , context={'doctors_detail':doctors_detail,})





def doctor_login(request):
    if request.method == 'POST':
        form = Login_Form
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)
        if user is not None :
            login(request , user)
            return redirect('doctor:doctors_list')
        else:
            messages.warning(request, "Username or password is incorrect. please try again")
    form  = Login_Form()
    return render(request , 'doctor/doctor_login.html' , context={'form':form})


@login_required
def doctor_logout(request):
    logout(request)
    return redirect(reverse('doctor:doctors_list'))



@login_required
def myprofile(request,slug):
    
    return render(request , 'doctor/doctor-myprofile.html' , context={})




















def signup(request):
    if request.method == 'POST':
        form2 = UserCreationForms(request.POST)
        if form2.is_valid():
            form2.save()

            return redirect('accounts:login')
    else:
        form2 = UserCreationForms
        

    return render(request , 'users/register.html' , context={'form2':form2})






@login_required
def delete_profile(request,id):
    single = User.objects.get(id=request.user.id)
    single.delete()
    return redirect(reverse('accounts:doctors_list'))


def update_profile(request):
    
    return render(request , 'users/updata_profile.html')


