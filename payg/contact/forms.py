from django import forms 

from djangular.forms import NgFormValidationMixin
from djangular.styling.bootstrap3.forms import (Bootstrap3Form,
    Bootstrap3ModelForm)

from contact.models import Contact, Newsletter


class FormNameAttr(object):
    def __init__(self):
        self.form_name = self.__class__.__name__


class ContactForm(FormNameAttr, NgFormValidationMixin, Bootstrap3ModelForm):
    class Meta:
        model = Contact
        fields = ['subject', 'name', 'email', 'message']


class NewsletterForm(FormNameAttr, NgFormValidationMixin, Bootstrap3ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
