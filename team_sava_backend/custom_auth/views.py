import datetime
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status, viewsets, mixins
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from .models import AuthUser, EmailToken
from .serializers import AuthUserSerializer, EmailTokenSerializer, PasswordResetSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = AuthUser.objects.all()
    serializer_class = AuthUserSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = super().get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = AuthUser.objects.create(**serializer.validated_data)
            user.set_password(serializer.validated_data['password'])
            user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        """
        User can only access his profile
        """
        if not self.request.user or str(self.request.user.id) != self.kwargs["pk"]:
            raise PermissionDenied
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        return obj


class EmailTokenViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = EmailToken.objects.all()
    serializer_class = EmailTokenSerializer
    http_method_names = ['get', 'post']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = super().get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            user = AuthUser.objects.filter(email=email).first()
            if user:
                user.send_password_reset_email()
        # return code 200 even if no users matching - All ok not to leak exisiting user email
        return Response({}, status=status.HTTP_200_OK)

    def get_object(self):
        """
        Object check if the expiration date is within time constaint
        """
        current_expiration = timezone.now() - datetime.timedelta(days=settings.TOKEN_VALID_DAYS)
        token = get_object_or_404(
            self.get_queryset(),
            id=self.kwargs["pk"],
            active=True,
        )
        if token.created_at < current_expiration:
            token.active = False
            token.save()
            raise NotFound
        return token


class PasswordResetView(CreateAPIView):
    queryset = EmailToken.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serialzier = super().get_serializer(data=request.data)
        if serialzier.is_valid(raise_exception=True):
            token = get_object_or_404(
                self.get_queryset(),
                pk=serialzier.validated_data['token'],
                active=True,
                created_at__gte=timezone.now() - datetime.timedelta(days=settings.TOKEN_VALID_DAYS)
            )
            user = token.user
            user.set_password(serialzier.validated_data['password1'])
            user.save()
            token.active = False
            token.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
