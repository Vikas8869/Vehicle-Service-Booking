from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import *
admin.site.register(Service)
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('user', 'created_at', 'expires_at')
    search_fields = ('user__username', 'otp')
    readonly_fields = ('created_at', 'expires_at')