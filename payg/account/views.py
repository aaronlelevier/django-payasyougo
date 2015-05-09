from django.views.generic import ListView
from django.views.generic.base import TemplateView

from rest_framework.response import Response
from rest_framework import generics, permissions

from braces.views import (LoginRequiredMixin, PermissionRequiredMixin,
    GroupRequiredMixin, SetHeadlineMixin, AnonymousRequiredMixin)

from account.models import AcctStmt, AcctTrans, Pricing
from account.serializers import PricingSerializer


class AccountView(LoginRequiredMixin, TemplateView):
    """
    Main Account View (Profile View of Hotel)
    """
    template_name = 'cpanel/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.request.user.profile.hotel
        return context


class AcctStmtListView(AdminOnlyMixin, SetHeadlineMixin, ListView):
    '''AcctStmt by Month.'''

    headline = _("Account Statements")
    template_name = 'list.html'

    def get_queryset(self):
        return AcctStmt.objects.filter(hotel=self.hotel)

    def get(self, request, *args, **kwargs):
        '''
        TODO: use a model method here.
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