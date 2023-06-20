from django.shortcuts import render , redirect
from django.urls import reverse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from doctor.models import Profile_Doctor , Schedule , Specialization
from .models import Client_Profile
from .forms import Login_Form , ClientSignupForm , ClienProfileForm , UserForm
from datetime import date as dt, datetime
from doctor.views import doc_home


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


def client_signup(request):
    if request.method == 'POST':
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username , password = password)
            login(request , user)
            return redirect('doctor:doctors_list')
    else:
        form = ClientSignupForm()
        

    return render(request , 'client/client-register.html' , context={'form':form})


@login_required
def update_client_profile(request ,  slug):
    client_profile = Client_Profile.objects.get(user = request.user)
    
    if request.method=='POST':
        userform = UserForm(request.POST , instance=request.user)
        client_profileform = ClienProfileForm(request.POST , request.FILES , instance=client_profile)
        if userform.is_valid() and client_profileform.is_valid():
            userform.save()
            myclient_profileform = client_profileform.save(commit=False)
            myclient_profileform.user = request.user
            myclient_profileform.save()
            return redirect(reverse('client:update_client_profile' , kwargs={'slug': client_profile.slug}))
    else:
        userform = UserForm(instance=request.user)
        client_profileform = ClienProfileForm(instance=client_profile)
    return render(request , 'client/client-profile-settings.html' , {'userform':userform ,'ClienProfileForm':client_profileform })



def test(request , slug):
    doctors_detail = Profile_Doctor.objects.get(slug = slug)

    return render(request , 'client/test.html' , {'doctors_detail':doctors_detail,})



@login_required
def my_appointments(request):
    client = Client_Profile.objects.get(user=request.user)
    today = Schedule.objects.filter(taken=client, date = dt.today())
    booked = Schedule.objects.filter(taken=client)
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    return render(request,'client/my_appointments.html', context={'client': client, 'booked':booked,'cancelled':cancelled, 'spec':spec, 'today': today})

@login_required
def client_home_doc(request , slug ):
    docs = Profile_Doctor.objects.get(slug = slug)
    client = Client_Profile.objects.get(user=request.user)
    booked = Schedule.objects.filter(taken=client , cancelled=client)
    today = Schedule.objects.filter(taken=client, date = dt.today())
    cancelled = Schedule.objects.filter(cancelled=client)
    doctor = Profile_Doctor.objects.get(slug=docs)
    doc_schedule = Schedule.objects.filter(doc=doctor)
    for sc in doc_schedule:
        if sc.date < dt.today() :
            sc.delete()
    doc_schedule = Schedule.objects.filter(doc=doctor)
    dates = sorted(set([sc.date for sc in doc_schedule]))
    

    return render(request, template_name=['client/booking.html','client/booking-success.html'] ,
                  context={ 'dates':dates ,'client': client, 'booked':booked, 
                           'cancelled':cancelled, 'doc_schedule':doc_schedule, 'doctor':doctor,  'today': today})


def booking_success(request , slug):
    docs = Profile_Doctor.objects.get(slug = slug)
    client = Client_Profile.objects.get(user=request.user)
    booked = Schedule.objects.filter(taken=client)
    today = Schedule.objects.filter(taken=client, date = dt.today())
    cancelled = Schedule.objects.filter(cancelled=client)
    doctor = Profile_Doctor.objects.get(slug=docs)
    doc_schedule = Schedule.objects.filter(doc=doctor)
    for sc in doc_schedule:
        if sc.date < dt.today() :
            sc.delete()
    doc_schedule = Schedule.objects.filter(doc=doctor)
    return render(request, template_name=['client/booking-success.html'] , context={ 'client': client, 'booked':booked, 'cancelled':cancelled, 'doc_schedule':doc_schedule, 'doctor':doctor,  'today': today})


@login_required
def book_slot(request, slot):
    user= User.objects.get(id = request.user.id)
    slot= Schedule.objects.get(id = slot)
    client = Client_Profile.objects.get(user=user)
    slot.taken = client
    slot.confirmed = False
    slot.save()
    return redirect(reverse('doctor:doctors_list')) 


@login_required
def delete_slot(request, slot):
    slot = Schedule.objects.get(id=slot)
    slot.delete()
    return redirect(reverse('client:client_home'))



""" def test2(request):
    return render(request , 'client/patient-dashboard.html' , {}) """



