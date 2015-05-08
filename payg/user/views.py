from django.shortcuts import render
from django.contrib import auth, messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from user.models import UserProfile
from user.serializers import UserProfileSerializer, UserSerializer, GroupSerializer
from account.helpers import login_messages


### Normal Auth Views n Redirects ###

@login_required(login_url=reverse_lazy('login'))
def private(request):
    messages.info(request, login_messages['now_logged_in'])
    return HttpResponseRedirect(reverse('account'))


def login_error(request):
    messages.warning(request, login_messages['login_error'])
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url=reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    messages.warning(request, 'You are now logged out')
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url=reverse_lazy('login'))
def verify_logout(request):
    return render(request, 'cpanel/form-success/verify_logout.html') # TODO: Make template


### REST ViewSets ###

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
