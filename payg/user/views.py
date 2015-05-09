from django.conf import settings
from django.shortcuts import render
from django.contrib import auth, messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, TemplateView
from django.forms.models import model_to_dict

from rest_framework import viewsets 
from braces.views import (AnonymousRequiredMixin, FormValidMessageMixin,
    LoginRequiredMixin, SetHeadlineMixin)

from user.models import UserProfile
from user.forms import UserCreateForm
from user.serializers import UserProfileSerializer, UserSerializer, GroupSerializer
from account.helpers import login_messages


@login_required(login_url=reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    messages.warning(request, 'You are now logged out')
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url=reverse_lazy('login'))
def verify_logout(request):
    return render(request, 'verify_logout.html')


class RegistrationView(AnonymousRequiredMixin, FormValidMessageMixin, CreateView):
    """Create a new User, login User, display 'loging success' msg."""
    model = User
    form_class = UserCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('account')
    authenticated_redirect_url = settings.VERIFY_LOGOUT_URL

    def get_form_valid_message(self):
        return "{0}, user account successfully created!".format(self.object.title)

    def form_valid(self, form):
        # Call super() so ``User`` object is available
        super().form_valid(form) 
        cd = form.cleaned_data

        # Login
        user = auth.authenticate(username=cd['username'], password=cd['password1'])
        if not user:
            raise forms.ValidationError(login_messages['no_match'])
        auth.login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


### User Views ###

class UserDetailView(LoginRequiredMixin, SetHeadlineMixin, TemplateView):
    template_name = 'profile.html'

    def get_headline(self):
        return "<em>{}'s</em> Home Page".format(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # populate user in the context w/o the password key
        user_dict = model_to_dict(self.request.user)
        user_dict.pop("password", None)
        context['user_dict'] = user_dict
        return context


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