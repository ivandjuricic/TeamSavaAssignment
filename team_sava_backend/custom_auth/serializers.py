from rest_framework import serializers
from .models import AuthUser, EmailToken


class AuthUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = AuthUser
        fields = [
            'id',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name'
        ]

    def validate(self, attrs):
        if attrs['password'] == attrs['password2']:
            attrs.pop('password2')
            return attrs
        raise serializers.ValidationError("Password missmatch")


class EmailTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = EmailToken
        fields = ['id', 'email']


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Password missmatch")
        return attrs
