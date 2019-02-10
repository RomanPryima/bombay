from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext as _

SUBJECT_CHOICES = (
    ('-----', '-----'),
    ('info', _('Request more information')),
    ('contribute', _('Learn more about how to contribute')),
    ('bug', _('Correction or bug report')),
    ('other', _('Other (please specify)'))
)


class ContactUsForm(forms.Form):
    name = forms.CharField(required=True, max_length=512)
    email = forms.EmailField(required=True)

    subject = forms.ChoiceField(
        required=True, choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': "form-control"}))

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': "form-control"}),
        required=True)

