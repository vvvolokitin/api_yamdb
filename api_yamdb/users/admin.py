from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import MyUser


class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = (
        "username", "email", "first_name", "last_name", "bio", "role"
    )
    list_editable = ("role",)
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Fields", {"fields": ("bio", "role")}),
    )


admin.site.register(MyUser, MyUserAdmin)
