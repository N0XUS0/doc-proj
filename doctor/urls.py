from django.urls import path 
from . import views


from django.urls import re_path as url

app_name  = 'doctor'


urlpatterns = [
    #path('test/' , views.test , name='update_profile'),
    #path('show_slot/', views.show_slot,name='show_slot'),

    path('add_slot/', views.add_slot,name='add_slot'),
    
    path('doc_home/', views.doc_home,name='doc_home'),
    
    #path('doc_home_slot/<str:date>/', views.doc_home_slot,name='doc_home_slot'),
    url(r'^doc_home_slot/(?P<date>\d{4}-\d{2}-\d{2})/$', views.doc_home_slot, name='doc_home_slot'),
    url(r'^delete_slot/(?P<slot>\d+)$', views.delete_slot, name='delete_slot'),



    # path('app/' , views.app , name='app')
    path('' , views.doctors_list , name='doctors_list'),
    path('login/' , views.doctor_login , name='login'),
    path('doctor_signup/' , views.signup , name='signup'),
    path('logout/' , views.doctor_logout , name='logout'),
    #path('<int:id>/myprofile/delete/' , views.delete_profile , name='profile_delete'),
    path('<slug:slug>/myprofile/' , views.myprofile , name='myprofile'),
    path('<slug:slug>/update_profile/' , views.update_profile , name='update_profile'),
    path('<slug:slug>/' , views.doctors_detail , name='doctor_detail'),

]








    #path('index/' , views.doctors_list2 , name='index2'),
