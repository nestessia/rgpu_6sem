from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailMessage, Drink


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['email']


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    model = Drink
    list_display = ['name', 'description', 'image']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at']
