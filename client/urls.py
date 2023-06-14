from django.urls import path
from . import views



app_name  = 'client'


urlpatterns = [
    #path('' , views.doctors_list , name='doctors_list'),
    path('login/' , views.client_login , name='login'),
    path('test/<slug:slug>/' , views.test , name='test'),

    
]