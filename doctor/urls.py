from django.urls import path
from . import views



app_name  = 'doctor'


urlpatterns = [
    # path('app/' , views.app , name='app')
    path('' , views.doctors_list , name='doctors_list'),
    path('login/' , views.doctor_login , name='login'),
    path('doctor_signup/' , views.signup , name='signup'),
    path('logout/' , views.doctor_logout , name='logout'),
    path('<int:id>/myprofile/delete/' , views.delete_profile , name='profile_delete'),
    path('<slug:slug>/myprofile/' , views.myprofile , name='myprofile'),
    path('update_profile/' , views.update_profile , name='update_profile'),
    
    path('<slug:slug>/' , views.doctors_detail , name='doctor_detail'),

]








    #path('index/' , views.doctors_list2 , name='index2'),
