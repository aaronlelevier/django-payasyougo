from django.contrib.auth import forms as auth_forms

from djangular.forms import NgFormValidationMixin
from djangular.styling.bootstrap3.forms import Bootstrap3Form


class AuthenticationForm(NgFormValidationMixin, auth_forms.AuthenticationForm, Bootstrap3Form):
    form_name = 'login_form'


class PasswordResetForm(NgFormValidationMixin, auth_forms.PasswordResetForm, Bootstrap3Form):
    form_name = 'pw_reset_form'


class SetPasswordForm(NgFormValidationMixin, auth_forms.SetPasswordForm, Bootstrap3Form):
    form_name = 'set_pw_form'


class PasswordChangeForm(NgFormValidationMixin, auth_forms.PasswordChangeForm, Bootstrap3Form):
    form_name = 'pw_change_form'