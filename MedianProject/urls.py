"""
URL configuration for MedianProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from MyApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    path('registration/', views.registration),
    path('login/', views.login),
    path('image/', views.image),
    path('your_images/', views.your_images)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
