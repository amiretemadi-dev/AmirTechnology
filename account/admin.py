from django.contrib import admin
from .models import CustomUser, VerificationCode

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'is_staff')
    search_fields = ('username',)
    search_help_text = 'You can search based on the user username.'


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'email')

