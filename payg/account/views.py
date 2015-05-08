import calendar

from django.conf import settings
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import auth, messages
from django.contrib.auth import REDIRECT_FIELD_NAME, views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, AnonymousUser

from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, FormMixin
from django.db.models import Avg, Max, Min, Sum

from rest_framework.response import Response
from rest_framework import generics, permissions, mixins

from braces.views import (LoginRequiredMixin, PermissionRequiredMixin,
    GroupRequiredMixin, SetHeadlineMixin, AnonymousRequiredMixin)

from account.decorators import anonymous_required
from account.forms import (AuthenticationForm, CloseAccountForm,
    CloseAcctConfirmForm, AcctCostCreateForm)
from account.helpers import login_messages
from account.models import AcctCost, AcctStmt, AcctTrans, Pricing
from account.serializers import PricingSerializer


### ACCOUNT VIEWS ###

class AccountView(LoginRequiredMixin, HotelUserMixin, TemplateView):
    """
    Main Account (profile) View.

    First time this is dispatched, make sure:
    - Hotel has a subaccount_sid
    - Assign a Twilio Ph #
    """
    template_name = 'cpanel/account.html'

    def get_context_data(self, **kwargs):
        '''TODO: clean up logic here b/4 produciton
            move `get_or_create` to a helper method?

            If move PhoneNumber.get_or_create + Subaccount.get_or_create
                to a Celery Job, can use:
                    `select_related() so only 1 query instead of 2?
        '''
        context = super().get_context_data(**kwargs)

        context['hotel'] = self.hotel

        return context


#############
# ACCT STMT #
#############

class AcctStmtListView(AdminOnlyMixin, SetHeadlineMixin, ListView):
    '''AcctStmt by Month.'''

    headline = _("Account Statements")
    template_name = 'list.html'

    def get_queryset(self):
        return AcctStmt.objects.filter(hotel=self.hotel)

    def get(self, request, *args, **kwargs):
        '''Ensure the current month's AcctStmt is up to date.

        TODO: Make this a daiy job, and not in the View.get()
        '''
        # acct_stmt = update_current_acct_stmt(hotel=self.hotel)
        return super().get(request, *args, **kwargs)


class AcctStmtDetailView(AdminOnlyMixin, TemplateView):
    '''
    All AcctTrans for a single Month.

    Organized in 4 blocks, by:
        Initial Monthly Balance
        Credits - detail
                - total
        Debits  - detail
                - total
        Balance - total
    '''
    template_name = 'account/acct_trans_detail.html'

    def get_context_data(self, **kwargs):
        '''
        TODO
        ----
        Move get custom `context` logic to a helper method to clean up view.
        '''
        context = super().get_context_data(**kwargs)

        # Use All Time Hotel Transactions to get the Balance
        all_trans = AcctTrans.objects.filter(hotel=self.hotel)

        # New Context
        context['init_balance'] = (all_trans.previous_monthly_trans(hotel=self.hotel,
                                                                    month=kwargs['month'],
                                                                    year=kwargs['year'])
                                            .balance())
        monthly_trans = (all_trans.monthly_trans(hotel=self.hotel,
                                                 month=kwargs['month'],
                                                 year=kwargs['year'])
                                  .order_by('created'))
        context['monthly_trans'] = monthly_trans
        context['balance'] = all_trans.balance()

        return context


########
# REST #
########

class PricingListAPIView(generics.ListAPIView):
    '''No permissions needed b/c read only list view, and will be used 
    on the Biz Site.'''

    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer

    def list(self, request, *args, **kwargs):
        '''For JSON Encoding.'''

        serializer = PricingSerializer(self.queryset, many=True)
        return Response(serializer.data)


class PricingRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer