import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from custom_auth.tasks import send_password_reset_email


class AuthUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class AuthUser(AbstractBaseUser):
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AuthUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # required abstract method for admin permissions
        #  no need for features here
        return True

    def has_module_perms(self, app_label):
        # required abstract method for admin permissions
        #  no need for features here
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def send_password_reset_email(self):
        """
        Creates a new EmailTokenObject and invoke async email sending celery task
        """
        token = EmailToken.objects.create(
            user=self
        )
        url = token.build_token_url()
        send_password_reset_email.delay(
            url, self.email, self.first_name
        )


class EmailToken(models.Model):
    """
    Model can be easily extended to be used for email confirmation
    and basically any email interaction user can have with email.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('AuthUser', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "({} {}) - {}".format(
            self.user.first_name,
            self.user.last_name, self.id
        )

    def build_token_url(self):
        """
        Builds frontend route for reset password form
        """
        return "{}/reset-password/{}".format(settings.DOMAIN, self.id)
