from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctor.models import Profile_Doctor, Schedule, Specialization
from .models import Client_Profile
from .forms import Login_Form, ClientSignupForm, ClientProfileForm, UserForm
from datetime import date as dt
import numpy as np
import PyPDF2

def client_login(request):
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('doctor:doctors_list')
            else:
                messages.warning(request, "اسم المستخدم أو كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى")
    else:
        form = Login_Form()
    return render(request, 'client/client_login.html', {'form': form})

def client_signup(request):
    if request.method == 'POST':
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('doctor:doctors_list')
    else:
        form = ClientSignupForm()
    return render(request, 'client/client-register.html', {'form': form})

@login_required
def update_client_profile(request, slug):
    try:
        client_profile = Client_Profile.objects.get(user=request.user)
    except Client_Profile.DoesNotExist:
        return redirect('client:client_signup')

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ClientProfileForm(request.POST, request.FILES, instance=client_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح')
            return redirect(reverse('client:update_client_profile', kwargs={'slug': client_profile.slug}))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ClientProfileForm(instance=client_profile)

    return render(request, 'client/client-profile-settings.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'client_profile': client_profile
    })

@login_required
def my_appointments(request):
    client = Client_Profile.objects.get(user=request.user)
    today = Schedule.objects.filter(taken=client, date=dt.today())
    booked = Schedule.objects.filter(taken=client)
    cancelled = Schedule.objects.filter(cancelled=client)
    spec = Specialization.objects.all()
    return render(request, 'client/patient-dashboard.html', {
        'client': client,
        'booked': booked,
        'cancelled': cancelled,
        'spec': spec,
        'today': today
    })
    
def booking2(request):
    return render(request, 'client/booking2.html', {})

@login_required
def test_ana(request):
    normal_results = {
        # Blood Picture
        'hgb': np.arange(13.5, 17.6, 0.1),
        'rbc': np.arange(4.3, 6.2, 0.1),
        'hct': np.arange(39, 52, 0.1),
        'mcv': np.arange(80, 101, 0.1),
        'mch': np.arange(27, 35, 0.1),
        'mchc': np.arange(32, 38, 0.1),
        'rdw': np.arange(11.5, 14.6, 0.1),
        'pct': np.arange(0.1, 0.6, 0.01),
        'mpv': np.arange(6.0, 12.1, 0.1),
        'wbc': np.arange(4.0, 11.1, 0.1),
        'neutrophil': np.arange(35, 81.1, 0.1),
        'lymphocytes': np.arange(18.0, 44.1, 0.1),
        'monocytes': np.arange(0, 10.0, 0.1),
        'eosinophils': np.arange(0, 4.1, 0.1),
        'basophils': np.arange(0, 1.1, 0.1),
        # Stool Examination
        # Physical Examination
        'odor': ['offensive'],
        'color': ["brownish"],
        'reaction': ['variable'],
        'mucus': ['absent'],
        'consistency': ['formed'],
        'food particles': ['absent'],
        # Microscopic Examination
        'trophozoite': ['absent'],
        'cysts': ['absent'],
        'ova': ['not detected'],
        'larva': ['absent'],
        'flagellates': ['absent'],
        'ciliate': ['absent'],
        'undigested food': ['absent'],
        'parasitology artifacts': ['absent']
    }

    if request.method == 'POST':
        file = request.FILES['file']
        pdf_reader = PyPDF2.PdfReader(file)

        page_text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text += page.extract_text()

        lines = page_text.split('\n')
        new_lines = []
        for line in lines:
            if ":" in line:
                new_lines.append(line)

        keys_in_text = []
        for key in normal_results:
            if key in page_text:
                keys_in_text.append(key)

        numbers = []
        for my_string in new_lines:
            try:
                number_string = my_string.split(":")[1].strip()
                number = float(number_string)
                numbers.append(number)
            except ValueError:
                numbers.append(number_string)

        patient_results = dict(zip(keys_in_text, numbers))

        newkey = []
        newvalue = []

        for key, value in patient_results.items():
            if isinstance(value, float):
                isB = np.isclose(normal_results[key], patient_results[key]).any()
                if not isB:
                    isB_str = str(normal_results[key]) == str(patient_results[key])
                    newkey.append(key)
                    newvalue.append(value)
                    if not isB_str:
                        print(f"Sorry, but you have a problem in '{key}' with result {value}")
            elif isinstance(value, str):
                isB_str = normal_results[key] == patient_results[key]
                if not isB_str:
                    print(f"Sorry, but you have a problem in '{key}' with result {value}") 

        return render(request, 'client/analysis.html', context={'newkey': newkey, 'newvalue': newvalue})

    # return an empty form
    return render(request, 'client/Analysis results.html')
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
    last_slog = Schedule.objects.last()
    return render(request, template_name=['client/booking-success.html'] , context={'docs':docs, 'last_slog':last_slog ,'client': client, 'booked':booked, 'cancelled':cancelled, 'doc_schedule':doc_schedule, 'doctor':doctor,  'today': today})

@login_required
def book_slot(request, slot):
    user= User.objects.get(id = request.user.id)
    slot= Schedule.objects.get(id = slot)
    client = Client_Profile.objects.get(user=user)
    slot.taken = client
    slot.confirmed = False
    slot.save()
    last_slog = Schedule.objects.last()

    #return redirect(reverse('doctor:doctors_list'))
    return render(request, 'client/checkout.html' , context={'last_slog':last_slog , 'slot':slot}) 

@login_required
def delete_slot(request, slot):
    slot = Schedule.objects.get(id=slot)
    slot.delete()
    return redirect(reverse('client:my-appointments'))



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
