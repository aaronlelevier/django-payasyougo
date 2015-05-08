from django import forms 
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import forms as auth_forms

from djangular.forms import NgFormValidationMixin
from djangular.styling.bootstrap3.forms import (Bootstrap3Form,
    Bootstrap3ModelForm)

from account.helpers import login_messages, salt
from account.models import AcctCost


#################
# DEFAULT FORMS #
#################

class AcctCostCreateForm(NgFormValidationMixin, Bootstrap3ModelForm):
    # djangular req
    form_name = 'acct_cost_create_form'

    class Meta:
        model = AcctCost
        fields = ['init_amt', 'balance_min', 'recharge_amt']


##############
# CLOSE ACCT #
##############

class CloseAccountForm(forms.Form):
    pass 


class CloseAcctConfirmForm(forms.Form):
    pass