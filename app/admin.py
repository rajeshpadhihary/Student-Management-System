from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import CustomUser,AdminHOD


class UserModel(UserAdmin):
    pass
admin.site.register(CustomUser,UserModel)

