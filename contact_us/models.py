from django.db import models
from django.utils.translation import ugettext_lazy as _


class Feedback(models.Model):
    user_name = models.CharField(_('Visitor Name'), max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    subject = models.CharField(_('Feedback Subject'), max_length=255, blank=True)
    message = models.TextField(_('Message'))

    publish = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    def __str__(self):
        return self.user_name
