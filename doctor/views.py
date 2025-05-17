from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.urls import reverse
from .models import Profile_Doctor , Doctor_Image , Schedule , Specialization
from .forms import Login_Form , SignupForm , UserForm , ProfileDoctorForm  , Complate_DocDate_Form
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date as dt, datetime
from .filters import DoctorFilter

from django.db.models.aggregates import Max , Min , Avg , Count , Sum

#from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.

""" def doctors_list2(request):
    doctors = User.objects.all()
    return render(request , 'users/index.html.html' , context={'doctors':doctors,})  """  
# doctor/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'doctor/index.html')

def welcome(request):
    return render(request,'doctor/doctors_list.html', context={})

    
def doctors_list(request):
    doctors = User.objects.all()
    specializations = Specialization.objects.all()

    return render(request , 'doctor/doctors_list.html' , context={'doctors':doctors,'specializations':specializations,})



def doctor_search(request):
    doctors = Profile_Doctor.objects.all()
    myfilter = DoctorFilter(request.GET,queryset=doctors)
    doctors = myfilter.qs

    return render(request , 'doctor/search.html' , context={'doctors':doctors , 'myfilter':myfilter,})

def doctor_patients(request,slug):
    doc = Profile_Doctor.objects.get(user=request.user)    

    schedule = Schedule.objects.filter(doc=doc)

    return render(request,'doctor/my-patients.html', context={ 'schedules':schedule,'doc':doc,})



def doctors_detail(request , slug):
    doctors_detail = Profile_Doctor.objects.get(slug = slug)
    return render(request , 'doctor/doctor-profile.html' , context={'doctors_detail':doctors_detail,})


@login_required
def myprofile(request,slug):
    return render(request , 'doctor/doctor-myprofile.html' , context={})


""" def show_Specialization(request):
    schedules = Schedule.objects.all()
    doc = Profile_Doctor.objects.get(user=request.user)    
    schedules = Schedule.objects.filter(doc=doc)
    return render(request , 'doctor/slot.html' , context={'schedules':schedules})
 """

def show_Specialization_detail(request,id):
    specializations = Specialization.objects.all()
    doc_specialization = Profile_Doctor.objects.filter(specialization=id)    
    return render(request , 'doctor/favourites.html' , context={'doc_specialization':doc_specialization , 'specializations':specializations,})


def doctor_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username , password = password)
            login(request , user)
            doctor_profile = Profile_Doctor.objects.get(user = request.user)
            return redirect(reverse('doctor:complate_doc_date' , kwargs={'slug': doctor_profile.slug}))
    else:
        form = SignupForm()
        

    return render(request , 'doctor/doctor-register.html' , context={'form':form})


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
    else:
        form  = Login_Form()
    return render(request , 'doctor/doctor_login.html' , context={'form':form})




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
            return redirect(reverse('doctor:update_profile' , kwargs={'slug': doctor_profile.slug}))
    else:
        userform = UserForm(instance=request.user)
        doctor_profileform = ProfileDoctorForm(instance=doctor_profile)
    return render(request , 'doctor/doctor-profile-settings.html' , {'userform':userform ,'doctor_profileform':doctor_profileform })



@login_required
def doctor_logout(request):
    logout(request)
    return redirect(reverse('doctor:doctors_list'))



@login_required
def doc_home(request):
    doc = Profile_Doctor.objects.get(user=request.user)
    schedule = Schedule.objects.filter(doc=doc)
    for sc in schedule:
        if sc.date < dt.today() :
            sc.delete()
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    return render(request,'doctor/schedule-timings.html', context={'doc':doc, 'dates':dates, 'today':today})





@login_required
def add_slot(request):
    if request.method == 'POST':
        doc = Profile_Doctor.objects.get(user=request.user)
        date = request.POST.get('date')
        start = request.POST.get('start')
        no_hours = int(request.POST.get('no_hours'))
        start =  str(datetime.strptime(str(int(start[:2])) +":"+ start[3:],"%H:%M"))[11:16]
        sc = Schedule(doc=doc, date=date, start_time=start, taken=None)
        sc.save()
        for _ in range(no_hours-1):
            start =  str(datetime.strptime(str(int(start[:2])+1) +":"+ start[3:],"%H:%M"))[11:16]
            sc = Schedule(doc=doc, date=date, start_time=start, taken=None)
            sc.save()
    return render(request,'doctor/schedule-timings.html', context={})
    
    

@login_required
def doc_home_slot(request, date):
    doc = Profile_Doctor.objects.get(user=request.user)    
    schedule = Schedule.objects.filter(doc=doc)
    for sc in schedule:
        if sc.date < dt.today() :
            sc.delete()
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    slot = Schedule.objects.filter(doc=doc, date=date)
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    t = str(dt.today())
    return render(request,'doctor/schedule-timings.html', context={'schedules':schedule,'t':t, 'doc':doc, 'dates':dates, 'slots':slot, 'date':date, 'today':today})


@login_required
def client_slot_list(request):
    doc = Profile_Doctor.objects.get(user=request.user)    
    schedule = Schedule.objects.filter(doc=doc)
    for sc in schedule:
        if sc.date < dt.today() :
            sc.delete()
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    slot = Schedule.objects.filter(doc=doc)
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    t = str(dt.today())
    return render(request,'doctor/appointments.html', context={'schedules':schedule,'t':t, 'doc':doc, 'dates':dates, 'slots':slot, 'today':today})

@login_required
def doctor_dashboard(request):
    doc = Profile_Doctor.objects.get(user=request.user)    
    schedule = Schedule.objects.filter(doc=doc)
    for sc in schedule:
        if sc.date < dt.today() :
            sc.delete()
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    slot = Schedule.objects.filter(doc=doc)
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    t = str(dt.today())
    
    slot_today_count= Schedule.objects.filter(doc=doc, date=dt.today()).count
    client_today_slot_count= Schedule.objects.filter(doc=doc ,confirmed=True , date=dt.today()).count
    client_all_slot_count= Schedule.objects.filter(doc=doc  ,confirmed=True).count
    return render(request,'doctor/doctor-dashboard.html', context={'client_all_slot_count':client_all_slot_count ,'client_today_slot_count':client_today_slot_count,'slot_today_count':slot_today_count, 'schedules':schedule,'t':t, 'doc':doc, 'dates':dates, 'slots':slot, 'today':today})





@login_required
def delete_slot(request, slot):
    slot = Schedule.objects.get(id=slot)
    date = slot.date
    slot.delete()
    return redirect(reverse('doctor:doc_home_slot', args=(date,)))



@login_required
def confirm_booking(request, slot):
    slot = Schedule.objects.get(id=slot)
    slot.confirmed = True
    slot.save()
    return redirect(reverse('doctor:client_slot_list'))


@login_required
def cancel_booking(request, slot):
    slot = Schedule.objects.get(id=slot)
    slot.confirmed=False
    slot.cancelled = slot.taken
    slot.taken=None
    slot.save()
    return redirect(reverse('doctor:client_slot_list'))




""" def delete_slot(request, slot):
    slot = Schedule.objects.get(id=slot)
    date = slot.date
    slot.delete()
    return HttpResponseRedirect(reverse('doctor:doc_home_slot', args=(date,))) """




def complate_doc_date(request ,  slug):
    doctor_profile = Profile_Doctor.objects.get(user = request.user)
    
    if request.method=='POST':
        docform = Complate_DocDate_Form(request.POST , instance=doctor_profile)
        if docform.is_valid():
            mydocform = docform.save(commit=False)
            mydocform.user = request.user
            mydocform.save()
            return redirect(reverse('doctor:compete_success'))
    else:
        mydocform = Complate_DocDate_Form(instance=doctor_profile)
    return render(request , 'doctor/complate_doc.html' , {'mydocform':mydocform })



def compete_success(request):
    
    return render(request , 'doctor/compete_success.html' , {})





def outocomplete(request):
    if 'term' in request.GET:
        qs = Profile_Doctor.objects.filter(name__icontains=request.GET.get('term'))
        names = list()
        for profile_doctor in qs:
            names.append(profile_doctor.name)
        return JsonResponse(names , safe=False)
            
    return render(request , 'doctor/doctors_list.html')
















""" @login_required
def doc_home_slot(request):
    doc = Profile_Doctor.objects.get(user=request.user)    
    schedule = Schedule.objects.filter(doc=doc)
    for sc in schedule:
        if sc.date < dt.today() :
            sc.delete()
    schedule = Schedule.objects.filter(doc=doc)
    dates = sorted(set([sc.date for sc in schedule]))
    slot = Schedule.objects.filter(doc=doc)
    today = Schedule.objects.filter(doc=doc, date=dt.today())
    t = str(dt.today())
    return render(request,'doctor/schedule-timings.html', context={'t':t, 'doc':doc, 'dates':dates, 'slots':slot, 'today':today}) """



""" @login_required
def delete_profile(request,id):
    single = User.objects.get(id=request.user.id)
    single.delete()
    return redirect(reverse('accounts:doctors_list')) """

def test(request):
    return render(request , 'doctor/doctor.html' , {})



""" def show_slot(request):
    schedules = Schedule.objects.all()
    doc = Profile_Doctor.objects.get(user=request.user)    
    schedules = Schedule.objects.filter(doc=doc)
    return render(request , 'doctor/slot.html' , context={'schedules':schedules}) """











