from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.core.validators import MaxValueValidator , MinValueValidator
from django.utils import timezone
from taggit.managers import TaggableManager

#from doctor.models import Profile_Doctor

# Create your models here.


GENDER_OPTION=(
    ('M','ذكر'),
    ('F','انتي'),
)

BLOOD_GROUP_OPTION = (
    ('A-','A-'),
    ('A+','A+'),
    ('B-','B-'),
    ('B+','B+'),
    ('AB-','AB-'),
    ('AB+','AB+'),
    ('O-','O-'),
    ('O+','O+'),
)

class Client_Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User") ,on_delete=models.CASCADE)
    name = models.CharField(_("الاسم"), max_length=50)
    image = models.ImageField(_("الصوره الشخصيه"), upload_to='client/profile/',null=True,blank=True)
    address = models.CharField(_("العنوان"), max_length=50 , null=True , blank=True)
    address_detail = models.CharField(_("تفاصيل العنوان"), max_length=500 , null=True , blank=True)
    number_phone = models.CharField(_("رقم الهاتف"), max_length=11 )
    gender = models.CharField(_("الجنس"), max_length=10 , choices=GENDER_OPTION)
    blood_group  = models.CharField(_("فصيله الدم "), max_length=5 , choices=BLOOD_GROUP_OPTION)
    date_of_birth = models.DateField(_("تاريخ الميلاد"), auto_now=False, auto_now_add=False , null=True , blank=True) 
    zip_code = models.IntegerField(_("Zip Code"), max_length=11 , null=True , blank=True)
    slug = models.SlugField(_("الاسم التعريفي") , null=True , blank=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
            
        super(Client_Profile, self).save(*args, **kwargs)
        


    def __str__(self):
        return '%s' %(self.user.username)

    class Meta:
        verbose_name = 'Client_Profile'
        verbose_name_plural = 'Client_Profiles'


def create_profile(sender , **kwargs):
    if kwargs['created']:
        client_profile = Client_Profile.objects.create(user=kwargs['instance'])
        
post_save.connect(create_profile,sender=User)