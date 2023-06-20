from django.urls import path
from . import views
from django.urls import re_path as url



app_name  = 'client'


urlpatterns = [
    path('my-appointments' , views.my_appointments , name='my-appointments'),
    path('booking_success/<slug:slug>/' , views.booking_success , name='booking_success'),
    path('loginclient/' , views.client_login , name='login'),
    path('client_signup/' , views.client_signup , name='client_signup'),
    url(r'book_slot/(?P<slot>\d+)$', views.book_slot, name='book_slot'),

    path('booking/<slug:slug>/' , views.client_home_doc , name='booking'),
    path('update_client_profile/<slug:slug>/' , views.update_client_profile , name='update_client_profile'),


    
]