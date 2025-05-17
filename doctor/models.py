from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.core.validators import MaxValueValidator , MinValueValidator
from django.utils import timezone
from taggit.managers import TaggableManager
from PIL import Image

from client.models import Client_Profile




GENDER_OPTION=(
    ('M','ذكر'),
    ('F','انثي'),
)

# Create your models here.

class Profile_Doctor(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User") ,on_delete=models.CASCADE)
    name = models.CharField(_("الاسم رباعي"), max_length=50)
    address = models.CharField(_("العنوان"), max_length=50 , null=True , blank=True)
    address_detail = models.CharField(_("العنوان بالتفصيل"), max_length=500, null=True , blank=True)
    subtitle = models.CharField(_("وصف مختصر"), max_length=100, null=True , blank=True)
    specialization = models.ForeignKey('Specialization',verbose_name='التخصص', related_name='profile_specialization' , on_delete=models.CASCADE , null=True , blank=True)
    specialist_doctor = models.CharField(_("متخصص في"), max_length=150 , null=True ,blank=True)
    price  = models.IntegerField(_("سعر الكشف") , null=True , blank=True)
    working_hours = models.IntegerField(_("ساعات العمل"), null=True , blank=True)
    waiting_time = models.IntegerField(_("وقت الانتظار"), null=True , blank=True)
    number_phone = models.CharField(_("رقم الهاتف"), max_length=11 , null=True , blank=True)

    gender = models.CharField(_("الجنس"), max_length=10 , choices=GENDER_OPTION , null=True , blank=True)
    who_i = models.CharField(_("من انا"), max_length=250 , null=True , blank=True)
    image = models.ImageField(_("الصوره"), upload_to='doctor/profile/',null=True,blank=True)
    join_us = models.DateTimeField(_("Join_Us"), auto_now=False, auto_now_add=True , null=True , blank=True)
    slug = models.SlugField(_("الاسم التعريفي") , null=True , blank=True)
    tags = TaggableManager(blank=True)
    active_doctor = models.BooleanField(_("active_doctor") , default=False)
    Syndicate = models.CharField(_("رقم التسجيل في النقابه"), max_length=50 )
    title = models.TextField(_("الوصف"), max_length=500, null=True , blank=True)

    fb_link = models.URLField(_("Facebook"), max_length=250 , null=True , blank=True)
    twit_link = models.URLField(_("Twitter"), max_length=200 , null=True , blank=True)
    google_link = models.URLField(_("Googlek"), max_length=200 , null=True , blank=True)
    



    def save(self, *args, **kwargs):
        
                
#        img = Image.open(self.image.path)
#        if img.height > 230 or img.width > 153:
#            output_size = (230 ,153 )
#            img.thumbnail(output_size)
#            img.save(self.image.path)
            
        if not self.slug:
            self.slug = slugify(self.user.username)
            
        if not self.who_i:
            self.who_i = slugify(self.name)
            
        super(Profile_Doctor, self).save(*args, **kwargs)
       

     
    
    def __str__(self):
        return '%s' %(self.user.username)

    class Meta:
        verbose_name = 'Profile_Doctor'
        verbose_name_plural = 'Profile_Doctors'
        
        
def create_profile(sender , **kwargs):
    if kwargs['created']:
        user_profile = Profile_Doctor.objects.create(user=kwargs['instance'])
        
post_save.connect(create_profile,sender=User)


    
    
class Specialization(models.Model):
    spec = models.CharField(_("التخصص"), max_length=200, unique=True)
    image = models.ImageField(_("الصوره"), upload_to='specialization_image/', null=True, blank=True)
    description = models.TextField(_("الوصف"), null=True, blank=True)
    
    def __str__(self):
        return self.spec

    class Meta:
        verbose_name = 'التخصص'
        verbose_name_plural = 'التخصصات'
        

class Doctor_Image(models.Model):
    doctor = models.ForeignKey(Profile_Doctor , related_name='image_doctor' ,on_delete=models.CASCADE)
    image = models.ImageField(_('Image'),upload_to='doctor/image_doctor/',null=True,blank=True)
    
    
    def __str__(self):
        return str(self.doctor)

    class Meta:
        verbose_name = 'Doctor_Image'
        verbose_name_plural = 'Doctor_Images'
        

    
class DoctorReview(models.Model):
    user = models.ForeignKey(User,related_name='user_review',on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile_Doctor,related_name='Profile_review',on_delete=models.CASCADE)
    rate = models.IntegerField(_('Rate'),validators=(MaxValueValidator(5),MinValueValidator(0)))
    create_at = models.DateTimeField(_('Create at'),default=timezone.now)
    review = models.CharField(_('Review'), max_length=500)


    def __str__(self):
        pass

    class Meta:
        verbose_name = 'DoctorReview'
        verbose_name_plural = 'DoctorReviews'
        
        

class Schedule(models.Model):
    doc = models.ForeignKey(Profile_Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    taken = models.ForeignKey(Client_Profile, related_name='taken_client', on_delete=models.CASCADE, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    cancelled = models.ForeignKey(Client_Profile, related_name='cancelled', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.doc) +" "+ str(self.date)