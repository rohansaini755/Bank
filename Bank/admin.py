# admin.py

from django.contrib import admin
from User.models import User, Otp, UserPersonalInfo

admin.site.register(User)
admin.site.register(Otp)
admin.site.register(UserPersonalInfo)
