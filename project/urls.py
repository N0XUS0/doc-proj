from django.contrib import admin
from django.urls import path, include
from doctor.views import doctors_list

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),  # تسجيل الدخول / تسجيل الخروج

    path('admin/', admin.site.urls),
    path('', doctors_list, name="mainpage"),  # الصفحة الرئيسية
    path('doctor/', include(('doctor.urls', 'doctor'), namespace='doctor')),
    path('client/', include(('client.urls', 'client'), namespace='client')),

    path('oauth/', include('social_django.urls', namespace='social')),  # تسجيل دخول فيسبوك أو غيره
]

# ملفات static و media في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
