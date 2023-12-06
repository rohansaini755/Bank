"""Bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from User import views as user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',user.login_page),
    path('send_otp/',user.send_otp),
    path('check/',user.check),
    path('verify/' , user.registration_verification),
    path('user_info/',user.user_info),
    path('user/<int:id>/',user.user_page),
    path('user_info/',user.user_info),
]

# urlpatterns += static(settings.STATIC_URl, document_root=settings.STATIC_ROOT)
