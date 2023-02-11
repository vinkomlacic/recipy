from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.forms import RecipyAuthenticationForm


class RecipyLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = RecipyAuthenticationForm
    next_page = reverse_lazy('recipy:index')
    extra_context = {
        'form_title': _('Login'),
        'form_submit_label': _('Login'),
    }
