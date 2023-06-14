from django.shortcuts import render , redirect
from django.urls import reverse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from doctor.models import Profile_Doctor
from .forms import Login_Form

# Create your views here.


def doctors_list(request):
    doctors = User.objects.all()
    return render(request , 'doctor/doctors_list.html' , context={'doctors':doctors,})


def doctors_detail(request , slug):
    doctors_detail = Profile_Doctor.objects.get(slug = slug)
    return render(request , 'doctor/doctor-profile.html' , context={'doctors_detail':doctors_detail,})





def client_login(request):
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
    else:
        form  = Login_Form()
    return render(request , 'cleint/client_login.html' , context={'form':form})










def test(request , slug):
    doctors_detail = Profile_Doctor.objects.get(slug = slug)

    return render(request , 'client/booking.html' , {'doctors_detail':doctors_detail,})