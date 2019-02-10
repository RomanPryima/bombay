from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.views.generic.edit import FormView

from contact_us.forms import ContactUsForm, SUBJECT_CHOICES
from contact_us.models import Feedback
from django.utils.translation import ugettext as _


class ContactUsView(FormView):
    template_name = 'contactus/contact_form.html'
    form_class = ContactUsForm
    success_url = "/contact/success/"
    subject = _("Contact Us Request")

    def get_initial(self):
        initial = super(ContactUsView, self).get_initial()
        if not self.request.user.is_anonymous:
            initial['name'] = self.request.user.get_full_name()
            initial['email'] = self.request.user.email
        initial['subject'] = 'info'
        return initial

    def form_invalid(self, form):
        return form.errors

    def form_valid(self, form):
        form_data = form.cleaned_data
        feedback = Feedback(
            user_name=form_data.get('name'),
            email=form_data.get('email'),
            subject=form_data.get('subject'),
            message=form_data.get('message'),
        )
        feedback.save()
        import pdb; pdb.set_trace()
        return super(ContactUsView, self).form_valid(form)
