from django.contrib import admin
from django.contrib import admin
from .models import GoogleToken

@admin.register(GoogleToken)
class GoogleTokenAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'updated_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'updated_at']

