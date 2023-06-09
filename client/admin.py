from django.contrib import admin
from .models import Client_Profile
# Register your models here.


#@admin.register(Client_Profile)
class Client_ProfileAdmin(admin.ModelAdmin):
    list_display = ['user' , 'name','gender']
    search_fields = ['name','blood_group']
    list_filter = ['gender','blood_group']





admin.site.register(Client_Profile,Client_ProfileAdmin)