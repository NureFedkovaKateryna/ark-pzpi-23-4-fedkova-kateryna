import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey('users.Role', on_delete=models.SET_NULL, null=True)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt_now = datetime.now()
        dt_exp = dt_now + timedelta(days=1)
        payload = {
            'user_id': self.pk,
            'email': self.email,
            'role': self.role.title,
            'iat': int(dt_now.timestamp()),
            'exp': int(dt_exp.timestamp()),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
