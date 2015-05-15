from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from contact import views


urlpatterns = patterns('',
    url(r'^two-forms/$', views.TwoFormView.as_view(), name='two_forms'),
    )