import django_filters
from .models import Profile_Doctor

class DoctorFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(label='Address' ,lookup_expr='icontains')
    address_detail = django_filters.CharFilter(label='Address Detail' , lookup_expr='icontains')
    name = django_filters.CharFilter(label='Name' , lookup_expr='icontains')
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    

    class Meta:
        model = Profile_Doctor
#        exclude = ['image' ,'tags','subtitle','user','number_phone']
        fields = ('name','gender','specialization','address','address_detail','price')
        
        
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key, None)
    except:
        return None
