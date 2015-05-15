from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from contact.models import Contact, Newsletter
from contact.forms import ContactForm, NewsletterForm


class TwoFormView(FormView):

    template_name = 'two_form.html'
    form_class = ContactForm
    second_form_class = NewsletterForm
    success_url = reverse_lazy('success')

    def get_context_data(self, **kwargs):
        context = super(TwoFormView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(initial={'some_field': context['model'].some_field})
        if 'form2' not in context:
            context['form2'] = self.second_form_class(initial={'another_field': context['model'].another_field})
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):

        # get the user instance
        self.object = self.get_object()

        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'form' in request.POST:

            # get the primary form
            form_class = self.get_form_class()
            form_name = 'form'

        else:

            # get the secondary form
            form_class = self.second_form_class
            form_name = 'form2'

        # get the form
        form = self.get_form(form_class)

        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})