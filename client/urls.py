from django.urls import path
from . import views
from django.urls import re_path as url



app_name  = 'client'


urlpatterns = [
    path('test2' , views.client_home , name='test2'),
    path('booking_success/<slug:slug>/' , views.booking_success , name='booking_success'),
    path('loginclient/' , views.client_login , name='login'),
    url(r'book_slot/(?P<slot>\d+)$', views.book_slot, name='book_slot'),

    path('booking/<slug:slug>/' , views.client_home_doc , name='booking'),

    
]