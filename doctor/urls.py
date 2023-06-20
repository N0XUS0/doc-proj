from django.urls import path 
from . import views


from django.urls import re_path as url

app_name  = 'doctor'


urlpatterns = [
    path('test/<int:id>' , views.show_Specialization_detail , name='show_Specialization_detail'),
    #path('show_slot/', views.show_slot,name='show_slot'),
    #path('test/', views.test,name='test'),

    path('add_slot/', views.add_slot,name='add_slot'),
    
    path('doc_home/', views.doc_home,name='doc_home'),
    
    #path('doc_home_slot/<str:date>/', views.doc_home_slot,name='doc_home_slot'),
    url(r'^doc_home_slot/(?P<date>\d{4}-\d{2}-\d{2})/$', views.doc_home_slot, name='doc_home_slot'),
    path('client_slot_list', views.client_slot_list, name='client_slot_list'),
    
    url(r'^delete_slot/(?P<slot>\d+)$', views.delete_slot, name='delete_slot'),
    url(r'^confirm_booking/(?P<slot>\d+)$', views.confirm_booking, name='confirm_booking'),

    url(r'^cancel_booking/(?P<slot>\d+)$', views.cancel_booking, name='cancel_booking'),



    # path('app/' , views.app , name='app')
    path('' , views.doctors_list , name='doctors_list'),
    path('login/' , views.doctor_login , name='login'),
    path('doctor_signup/' , views.doctor_signup , name='doctor_signup'),
    path('logout/' , views.doctor_logout , name='logout'),
    #path('<int:id>/myprofile/delete/' , views.delete_profile , name='profile_delete'),
    path('<slug:slug>/myprofile/' , views.myprofile , name='myprofile'),
    path('<slug:slug>/update_profile/' , views.update_profile , name='update_profile'),
    path('<slug:slug>/' , views.doctors_detail , name='doctor_detail'),

]








    #path('index/' , views.doctors_list2 , name='index2'),
