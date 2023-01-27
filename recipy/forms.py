from crispy_forms.helper import FormHelper
from django import forms
from django.utils.translation import gettext_lazy as _

from recipy.models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = '__all__'
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'duration_minutes': _('Duration (in minutes)'),
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
