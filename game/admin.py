from django.contrib import admin

from .models import MainUser, SubUser
# Register your models here.
admin.site.register(MainUser)
admin.site.register(SubUser)