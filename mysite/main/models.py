from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
import uuid
from django.db.models import signals
from django.core.mail import send_mail
from .tasks import send_verification_email
from django.urls import reverse

class UserAccountManager(BaseUserManager):
    use_in_migrations = True


    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email not found')
        if not password:
            raise ValueError('password not found')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField('email', unique=True, blank=False, null=False)
    full_name = models.CharField('full name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)  # Добавили `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    def get_short_name(self):
        return self.email


    def get_full_name(self):
        return self.email


    def __unicode__(self):
        return self.email


    def user_post_save(sender, instance, signal, *args, **kwargs):
        if not instance.is_verified:
            # Send verification email
            send_verification_email.delay(instance.pk)
# метод .delay объекта задачи. Это означает, что мы отправляем
# задание на Celery, и мы не ожидаем результата.

    signals.post_save.connect(user_post_save, sender=User)

