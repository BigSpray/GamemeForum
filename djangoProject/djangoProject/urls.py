"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path as url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user.views import UserViews, UserDataViews,UserShowDataViews
from django.views.static import serve
from djangoProject.settings import MEDIA_ROOT
from djangoProject.settings import MEDIA_URL
from djangoProject import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

router.register(r'user', UserViews, basename='user')
router.register(r'userdata', UserDataViews, basename='userdata')
router.register(r'usershowdata', UserShowDataViews, basename='usershowdata')

urlpatterns = [
    url('', include(router.urls)),
    url('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'upimg/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('', include('user.urls')),
    path('', include('material.urls')),
    path('', include('blog.urls')),
]

INSTALLED_APPS = [
    'drf_yasg',  # swagger
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)