from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    fieldsets = UserAdmin.fieldsets + (
            (
                "Custom Profile",
                {
                    "fields":(
                        'avatar',
                        'gender',
                        'bio',
                        'birthdate',
                        'language',
                        'currency',
                        'superhost',
                        'login_method',
                )
            }
        ),
    )


    list_filter = UserAdmin.list_filter + (
        "superhost",
    )

    list_display = (
        'id',
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        'login_method',

    )




""" 기본 모델"""
# @admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):
#
#     """Custom User Admin"""
#
#     list_display = ('id','email','username','gender','language','currency','superhost')
#     list_filter = ("language","currency","superhost",)






