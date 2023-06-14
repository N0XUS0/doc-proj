from django.contrib import admin
from .models import Profile_Doctor ,Doctor_Image , Specialization , Schedule

# Register your models here.


""" class Profile_Admin(admin.ModelAdmin):
    list_display = ('name', 'price') """

class ProfileImageTabular(admin.TabularInline):
    model=Doctor_Image
    
class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileImageTabular]
    


admin.site.register(Profile_Doctor,ProfileAdmin)  #(Profile_Admin)
admin.site.register(Doctor_Image)
admin.site.register(Specialization)
admin.site.register(Schedule)