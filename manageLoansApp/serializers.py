# serializers.py

from rest_framework import serializers
from .models import UserProfile, Loan, Transaction, EMI

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class EMISerializer(serializers.ModelSerializer):
    class Meta:
        model = EMI
        fields = '__all__'
