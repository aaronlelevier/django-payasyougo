from django.db import models

from account.models import TimeStampBase


class Contact(TimeStampBase):
	subject = models.CharField(max_length=100)
	name = models.CharField(blank=True, max_length=100)
	email = models.EmailField()
	message = models.CharField(max_length=100)


class Newsletter(TimeStampBase):
	email = models.EmailField()
