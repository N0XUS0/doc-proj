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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import PyPDF2
import numpy as np
import cv2
from deepface import DeepFace
@login_required
def test_ana(request):
    normal_ranges = {
        "hgb": (13.5, 17.5),
        "rbc": (4.3, 6.2),
        "hct": (39, 52),
        "mcv": (80, 100),
        "mch": (27, 34),
        "mchc": (32, 36),
        "rdw": (11.5, 14.5),
        "pct": (0.15, 0.5),
        "mpv": (6.0, 12.0),
        "wbc": (4.0, 11.0),
        "neutrophil": (35, 80),
        "lymphocytes": (18, 44),
        "monocytes": (0, 10),
        "eosinophils": (0, 4),
        "basophils": (0, 1)
    }

    diseases_specializations = {
        "فقر دم (Anemia)": ["هيماتولوجيا", "باطنة"],
        "احتمال عدوى (Infection)": ["ميكروبيولوجيا", "أمراض معدية"],
    }

    if request.method == "POST":
        file = request.FILES['file']
        pdf = PyPDF2.PdfReader(file)
        content = ""
        for page in pdf.pages:
            content += page.extract_text()

        # استخراج القيم
        values = {}
        for line in content.split("\n"):
            parts = line.strip().split(":")
            if len(parts) == 2:
                key = parts[0].strip().lower()
                try:
                    value = float(parts[1].strip())
                    values[key] = value
                except:
                    pass

        # تحليل القيم
        abnormal_keys = []
        abnormal_values = []
        for key, value in values.items():
            if key in normal_ranges:
                low, high = normal_ranges[key]
                if value < low or value > high:
                    abnormal_keys.append(key)
                    abnormal_values.append(value)

        # تشخيص الحالة وربطها بالتخصصات
        matched_diseases = []
        suggested_specializations = []
        
        for disease_name, disease_keys in diseases_specializations.items():
            if any(key in abnormal_keys for key in normal_ranges):
                matched_diseases.append(disease_name)
                suggested_specializations.extend(disease_keys)

        # جلب الأطباء المقترحين
        suggested_doctors = Profile_Doctor.objects.filter(
            specialization__spec__in=suggested_specializations,
            active_doctor=True
        ).select_related('specialization')[:5]  # عرض أول 5 أطباء

        # حالة المريض
        if not matched_diseases:
            status = "✅ المريض سليم"
        elif len(matched_diseases) == 1:
            status = f"❗ محتمل وجود: {matched_diseases[0]}"
        else:
            status = "🚨 يوجد أكثر من مؤشر مرضي: " + "، ".join(matched_diseases)

        return render(request, 'client/analysis.html', {
            'newkey': abnormal_keys,
            'newvalue': abnormal_values,
            'status': status,
            'suggested_doctors': suggested_doctors,
            'matched_diseases': matched_diseases,
            'suggested_specializations': list(set(suggested_specializations))
        })

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
