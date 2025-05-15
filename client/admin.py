from django.contrib import admin
from .models import Client_Profile

class Client_ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'gender', 'blood_group']
    search_fields = ['name', 'blood_group', 'user__username']
    list_filter = ['gender', 'blood_group']
    readonly_fields = ['slug']

admin.site.register(Client_Profile, Client_ProfileAdmin)