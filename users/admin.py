from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_active", "password", "avatar", "phone_number")
    list_filter = ("email",)
    search_fields = ("email",)
