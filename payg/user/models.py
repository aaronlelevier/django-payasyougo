from django.db import models
from django.contrib.auth.models import User

from account.models import TimeStampBase, Hotel


class UserProfile(TimeStampBase):
    user = models.ForeignKey(User, related_name="profile")
    hotel = models.ForeignKey(Hotel)

    def __str__(self):
        return self.user.username