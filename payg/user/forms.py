from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from djangular.forms import NgFormValidationMixin
from djangular.styling.bootstrap3.forms import (Bootstrap3Form,
    Bootstrap3ModelForm)


class AuthenticationForm(NgFormValidationMixin, auth_forms.AuthenticationForm, Bootstrap3Form):
    form_name = 'login_form'


class PasswordResetForm(NgFormValidationMixin, auth_forms.PasswordResetForm, Bootstrap3Form):
    form_name = 'pw_reset_form'


class SetPasswordForm(NgFormValidationMixin, auth_forms.SetPasswordForm, Bootstrap3Form):
    form_name = 'set_pw_form'


class PasswordChangeForm(NgFormValidationMixin, auth_forms.PasswordChangeForm, Bootstrap3Form):
    form_name = 'pw_change_form'



# import re

# from django import forms
# from django.conf import settings
# from django.contrib import auth, messages
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User, Group
# from django.utils.translation import ugettext, ugettext_lazy as _
# from django.utils import six



class UserCreateForm(NgFormValidationMixin, Bootstrap3ModelForm):
    '''Form for creating new Users. 

    Structure based off of: ``django.contrib.auth.forms.UserCreationForm``
    '''
    form_name = 'user_create_form'

    # UserCreationForm
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    # because I want to require these fields, and the Django model
    # doesn't require them by default
    first_name = forms.CharField(label=_("First Name"), required=True)
    last_name = forms.CharField(label=_("Last Name"), required=True)
    email = forms.EmailField(label=_("Email"), required=True)

    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-_]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
            'username', 'password1', 'password2',)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user