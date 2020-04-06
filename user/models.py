from __future__ import unicode_literals

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, shopAdmin=False):
        if not email:
            return ValueError('Email pls')
        client = self.model(
            name=name,
            email=email,
            shopAdmin=shopAdmin
        )
        client.set_password(password)
        client.save(using=self._db)
        return client

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            name=name,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.CharField(primary_key=True, max_length=200, verbose_name='email')
    name = models.CharField(max_length=200, verbose_name='Full name')

    shopAdmin = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    latitude = models.DecimalField(decimal_places=7, max_digits=11, null=True)
    longitude = models.DecimalField(decimal_places=7, max_digits=11, null=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def get_short_name(self):
        return self.name.split(' ')[0]

    def get_full_name(self):
        return self.name

    @property
    def is_superuser(self):
        return self.admin
