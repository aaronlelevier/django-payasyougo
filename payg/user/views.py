from django.shortcuts import render
from django.contrib import auth, messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from account.helpers import login_messages


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
    

class AdminCreateView(RegistrationContextMixin, CreateView):
    """
    Step #1 of Registration

    Purpose:
        - Create a new User
        - Add them to the "hotel_admin" Group
        - Log in User
    """
    model = User
    form_class = UserCreateForm
    template_name = 'frontend/register.html'
    success_url = reverse_lazy('main:register_step2')
    authenticated_redirect_url = settings.VERIFY_LOGOUT_URL

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






