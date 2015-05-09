from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from user import views
from user.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm,
    PasswordChangeForm)


urlpatterns = patterns('',

    # Registration Views
    url(r'^login/$',auth_views.login,
        {'template_name': 'form.html',
        'authentication_form': AuthenticationForm,
        'redirect_field_name': '/',
        'extra_context': {
            'headline': 'Login Form'
            }
        },
        name='login'),

    ### 2 views for password change - when you are logged in and want to 
    ### change your password
    url(r'^password_change/$', auth_views.password_change,
        {'template_name': 'cpanel/auth-forms/password_change.html',
        'password_change_form': PasswordChangeForm},
        name='password_change'),

    url(r'^password_change/done/$', auth_views.password_change_done,
        {'template_name': 'cpanel/form-success/password_change_done.html'},
        name='password_change_done'),

    ### 4 views for password reset when you can't remember your password
    url(r'^password_reset/$', auth_views.password_reset,
        {
        'template_name': 'cpanel/auth-forms/password_reset.html',
        'email_template_name': 'email/password_reset.html',
        'subject_template_name': 'registration/password_reset_subject.txt',
        'password_reset_form': PasswordResetForm,
        'extra_context': {
            'headline': 'Forgot Password?'
            }
        },
        name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'cpanel/form-success/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name':'cpanel/auth-forms/password_reset_confirm.html',
        'set_password_form': SetPasswordForm
        }, name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'cpanel/form-success/password_reset_complete.html'},
        name='password_reset_complete'),

    ### My Auth Views
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^verify-logout/$', views.verify_logout, name='verify_logout'),

    ### User Views
    url(r'^accounts/profile/$', views.UserDetailView.as_view(), name='user_detail'),
)





