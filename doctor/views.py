from django.shortcuts import render , redirect
from django.urls import reverse
from .models import Profile_Doctor , Doctor_Image
from .forms import Login_Form , SignupForm , UserForm , ProfileDoctorForm , Doctor_Image_form
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




def doctor_login(request):                               #! اعمل اضافه لي method == get 
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
    return render(request , 'doctor/doctor_login.html' , context={'form':form})




def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username , password = password)
            login(request , user)
            return redirect('doctor:doctors_list')
    else:
        form = SignupForm()
        

    return render(request , 'doctor/doctor-register.html' , context={'form':form})




@login_required
def update_profile(request ,  slug):
    doctor_profile = Profile_Doctor.objects.get(user = request.user)
    
    if request.method=='POST':
        userform = UserForm(request.POST , instance=request.user)
        doctor_profileform = ProfileDoctorForm(request.POST , request.FILES , instance=doctor_profile)
        if userform.is_valid() and doctor_profileform.is_valid():
            userform.save()
            mydoctor_profileform = doctor_profileform.save(commit=False)
            mydoctor_profileform.user = request.user
            mydoctor_profileform.save()
            return redirect(reverse('doctor:myprofile' , kwargs={'slug': doctor_profile.slug}))
    else:
        userform = UserForm(instance=request.user)
        doctor_profileform = ProfileDoctorForm(instance=doctor_profile)
    return render(request , 'doctor/doctor-profile-settings.html' , {'userform':userform ,'doctor_profileform':doctor_profileform })



@login_required
def doctor_logout(request):
    logout(request)
    return redirect(reverse('doctor:doctors_list'))


@login_required
def myprofile(request,slug):
    return render(request , 'doctor/doctor-myprofile.html' , context={})



    
    




@login_required
def delete_profile(request,id):
    single = User.objects.get(id=request.user.id)
    single.delete()
    return redirect(reverse('accounts:doctors_list'))













def test(request):
    return render(request , 'doctor/doctor-profile-settings.html' , {})