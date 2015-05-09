from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from account.models import TimeStampBase, Hotel


class UserProfile(TimeStampBase):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    hotel = models.ForeignKey(Hotel, blank=True, null=True)

    def __str__(self):
        return self.user.username


'''
UserProfile is a OneToOne to User, and should not exist unless there
is a User. So Auto create/delete based on User.
'''
@receiver(post_save, sender=User)
def create_userprofile(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(pre_delete, sender=User)
def delete_userprofile(sender, instance=None, **kwargs):
    if instance:
        userprofile = UserProfile.objects.get(user=instance)
        userprofile.delete()