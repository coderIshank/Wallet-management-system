from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Wallet, Transaction


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user  


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']
        read_only_fields = ['balance']


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class CreditDebitSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = serializers.CharField(max_length=200)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        
        return value

