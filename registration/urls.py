from django.urls import path
from .views import (
    DelegateCardRegisterView,
    verify_registration,
    export_verified_delegate_cards,
    EventRegisterView,
    verify_event_registration,
    export_verified_event_registrations,
    PassPurchaseView,
    verify_pass,
    export_verified_passes,
)

urlpatterns = [
    path('delegate-card/', DelegateCardRegisterView.as_view(), name='delegate-card-register'),
    path('delegate-card/verify/<int:pk>/', verify_registration, name='delegate-card-verify'),
    path('delegate-card/export/', export_verified_delegate_cards, name='delegate-card-export'),

    path('event-register/', EventRegisterView.as_view(), name='event-register'),
    path('event-register/verify/<int:pk>/', verify_event_registration, name='event-register-verify'),
    path('event-register/export/', export_verified_event_registrations, name='event-register-export'),

    path('pass-purchase/', PassPurchaseView.as_view(), name='pass-purchase'),
    path('pass-purchase/verify/<int:pk>/', verify_pass, name='verify-pass'),
    path('pass-purchase/export/', export_verified_passes, name='export-pass'),
]
