from django.contrib.auth.models import BaseUserManager
from rest_framework.exceptions import ValidationError
from .models import Role, Organisation


class UserManager(BaseUserManager):

    def create_user(self, email, username, password, organisation_title, role=None, **extra_fields):
        if not email:
            raise ValidationError('Users must have an email')

        if not username:
            raise ValidationError('Users must have a username')

        if not password:
            raise ValidationError('Users must have a password')

        if not organisation_title:
            raise ValidationError('Users must have an organisation title')

        role = Role.objects.get(title=role)
        organisation = Organisation.objects.create(title=organisation_title)

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role_id=role.role_id,
            organisation_id=organisation.organisation_id,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, None, 'Admin', **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
