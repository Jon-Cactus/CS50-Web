from django.contrib import admin
from .models import Email, User

# Register your models here.

class EmailAdmin(admin.ModelAdmin):
    list_display = ("user", "sender", "recipients", "subject", "body", "timestamp", "read", "archived")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")

admin.site.register(User)
admin.site.register(Email)