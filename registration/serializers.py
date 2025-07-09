from rest_framework import serializers
from .models import DelegateCardRegistration, EventRegistration, PassPurchase

class DelegateCardRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DelegateCardRegistration
        fields = '__all__'
        read_only_fields = ['amount', 'is_verified', 'created_at']


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'


class PassPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassPurchase
        fields = '__all__'
        read_only_fields = ['amount', 'is_verified', 'verified_at', 'created_at']