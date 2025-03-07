from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP

User = get_user_model()


def clean_email(value):
    if 'admin' in value:
        raise serializers.ValidationError('admin cant be in email.')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email,)}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField(write_only=True)


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('code',)

