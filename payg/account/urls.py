from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from account import views
from account.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm,
    PasswordChangeForm)


acct_stmt_patterns = patterns('',
    url(r'^$', views.AcctStmtListView.as_view(), name='acct_stmt_list'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.AcctStmtDetailView.as_view(), name='acct_stmt_detail'),
    )

account_patterns = patterns('',
    # Main Profile View
    url(r'^$', views.AccountView.as_view(), name='account'),
)

urlpatterns = patterns('',
    url(r'^account/', include(account_patterns)),
    url(r'^statements/', include(acct_stmt_patterns)),
    )