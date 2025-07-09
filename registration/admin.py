from django.contrib import admin
from .models import DelegateCardRegistration, EventRegistration

@admin.register(DelegateCardRegistration)
class DelegateCardAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'tier', 'is_verified', 'verified_at', 'created_at')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
  list_display = ('name', 'email', 'amount', 'is_verified', 'verified_at', 'created_at')
  list_filter = ('is_verified',)