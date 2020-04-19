from django.test import TestCase
from rest_framework import serializers
from custom_auth.tests.factories import EmailTokenFactory
from custom_auth.serializers import AuthUserSerializer, EmailTokenSerializer, PasswordResetSerializer


class TestAuthSerializer(TestCase):

    def setUp(self):
        self.data = {
            "first_name": "TestFirstName",
            "last_name": "TestLastname",
            "email": "test@testemail.com",
            "password": "TestPassword1",
            "password2": "TestPassword1"
        }

    def test_valdate_success(self):
        serializer = AuthUserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_fail_missing_fields(self):
        required_fields = (
            'email',
            'password',
            'password2',
            'first_name',
            'last_name'
        )
        for field in required_fields:
            data = dict(self.data)
            data.pop(field)
            serializer = AuthUserSerializer(data=data)
            self.assertFalse(serializer.is_valid(), field)

    def test_fail_password_missmatch(self):
        self.data['password2'] = "WrongPassword"
        serializer = AuthUserSerializer(data=self.data)
        with self.assertRaises(serializers.ValidationError):  # showcase different assertions :)
            serializer.is_valid(raise_exception=True)


class TestEmailTokenSerializer(TestCase):

    def test_serialzier_valid(self):
        data = {
            "id": "123123",
            "email": "test_emal@testemail.com",
        }
        serializer = EmailTokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_not_valid_missing_email(self):
        data = {
            "id": "123123",
        }
        serializer = EmailTokenSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serialzier_representation(self):
        token = EmailTokenFactory()
        serializer = EmailTokenSerializer()
        output = serializer.to_representation(token)
        self.assertTrue('id' in output, 'id missing')


class TestPasswordResetSerializer(TestCase):

    def setUp(self):
        self.data = {
            "token": "12321",
            "password1": "test_password1",
            "password2": "test_password1",
        }

    def test_serializer_valid(self):
        serializer = PasswordResetSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_not_valid_missing_parameter(self):
        required_params = ['token', 'password1', 'password2']
        for param in required_params:
            data = dict(self.data)
            data.pop(param)
            serializer = PasswordResetSerializer(data=data)
            self.assertFalse(serializer.is_valid())

    def test_passwords_missmatch(self):
        self.data['password2'] = "DifferetnPassword"
        serializer = PasswordResetSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
