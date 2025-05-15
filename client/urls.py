from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('booking2/', views.booking2, name='booking2'),
    path('test-ana/', views.test_ana, name='test-ana'),
    path('my-appointments/', views.my_appointments, name='my-appointments'),
    path('booking_success/<slug:slug>/', views.booking_success, name='booking_success'),
    path('loginclient/', views.client_login, name='login'),
    path('client_signup/', views.client_signup, name='client_signup'),
    path('book_slot/<int:slot>/', views.book_slot, name='book_slot'),
    path('delete_slot/<int:slot>/', views.delete_slot, name='delete_slot'),
    path('booking/<slug:slug>/', views.client_home_doc, name='booking'),
    path('update_client_profile/<slug:slug>/', views.update_client_profile, name='update_client_profile'),
]