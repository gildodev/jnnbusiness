
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app import urls, views


urlpatterns = [
    path('',include(urls)),
    path('admin', admin.site.urls, name='admins'),
    path('admin/', admin.site.urls, name='admins'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)