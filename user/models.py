from __future__ import unicode_literals

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            return ValueError('Email pls')
        client = self.model(
            name=name,
            email=email,
        )
        client.set_password(password)
        client.save(using=self._db)
        return client

    def create_shopadmin(self, email, name, password):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_shopAdmin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.CharField(unique=True, max_length=200, verbose_name='Email')
    name = models.CharField(max_length=200, verbose_name='Full name')
    created_time = models.DateTimeField(default=timezone.now)

    is_shopAdmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    latitude = models.DecimalField(decimal_places=7, max_digits=11, null=True)
    longitude = models.DecimalField(decimal_places=7, max_digits=11, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def get_short_name(self):
        return self.name.split(' ')[0]

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

    def is_client(self):
        return not self.is_admin and not self.is_shopAdmin
    is_client.boolean = True

    def __str__(self):
        return self.email
