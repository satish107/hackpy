# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.

class UserProfileManager(BaseUserManager):
	def create_user(self, email, username, password = None, commit = True):
		if not email:
			raise ValueError("users must have an email address")
		if not username:
			raise ValueError("users must have username")

		user = self.model(
			email = self.normalize_email(email),
			username = username,
			)
		user.set_password(password)
		if commit:
			user.save(using = self._db)

		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
				email,
				username = username,
				password = password,
				commit = False
			)
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name = 'email address', max_length = 50, unique = True)
	username = models.CharField(verbose_name = 'username', max_length = 50, null = True, blank = True)
	is_active = models.BooleanField('active', default = True)
	is_staff = models.BooleanField('staff status', default = True)
	date_joined = models.DateTimeField(default = timezone.now)

	objects = UserProfileManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.username

	def get_short_name(self):
		return self.username





