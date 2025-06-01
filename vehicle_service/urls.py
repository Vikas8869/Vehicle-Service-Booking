"""
URL configuration for vehicle_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from service.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',index,name="index"),
    path('',home_page,name="home_page"),
    path('aboutus/',aboutus,name="aboutus"),
    path('charges/',charges,name="charges"),
    path('service_page/',service_page,name="service_page"),
    path('service_view/',service_view,name="service_view"),
    path('contact_page/',contact_page,name="contact_page"),
    path('service_update/<id>/',service_update,name="service_update"),
    path('cancel_service/<id>/',cancel_service,name="cancel_service"),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/forgot-password/',forgot_password_view, name='forgot_password'),
    path('accounts/verify-otp/',verify_otp_view, name='verify_otp'),
    path('accounts/reset-password/',reset_password_view, name='reset_password'),

]
