from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class RecipyAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove field labels and add placeholders instead
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = _('Username')
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = _('Password')
