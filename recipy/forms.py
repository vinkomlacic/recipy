from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from recipy.models import Recipe, Step, Ingredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'duration_minutes')
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'duration_minutes': _('Duration (in minutes)'),
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.instance.user = user

        self.helper = FormHelper()
        self.helper.form_tag = False

        # Initialize formsets
        self.step_formset = RecipeStepFormSet(
            data=kwargs.get('data'), files=kwargs.get('files'),
            instance=self.instance,
            form_kwargs={'inline': True, 'formset_form': True}
        )
        self.ingredient_formset = RecipeIngredientFormSet(
            data=kwargs.get('data'), files=kwargs.get('files'),
            instance=self.instance,
            form_kwargs={'inline': True, 'formset_form': True}
        )

    def is_valid(self):
        is_valid = super().is_valid()
        is_valid &= self.step_formset.is_valid()
        is_valid &= self.ingredient_formset.is_valid()

        return is_valid

    def save(self, **kwargs):
        # First save the base instance
        saved_recipe = super().save(**kwargs)

        # Then save the formsets. Replace the instance with the saved one
        # because the initial ones don't have PK in create forms.
        self.step_formset.instance = saved_recipe
        self.step_formset.save()

        self.ingredient_formset.instance = saved_recipe
        self.ingredient_formset.save()


class StepForm(forms.ModelForm):

    class Meta:
        model = Step
        fields = '__all__'

        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'duration_minutes': _('Duration (in minutes)'),
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        inline = kwargs.pop('inline', False)
        formset_form = kwargs.pop('formset_form', False)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        if formset_form:
            # In the context of formset, this is necessary because we need the
            # ID field.
            self.helper.render_hidden_fields = True

            # In a formset, this cannot be enforced anyway
            self.fields['name'].required = False

        if inline:
            self.helper.layout = Layout(
                Row(Column('name'), Column('duration_minutes')),
                Row(Column('description'))
            )


RecipeStepFormSet = inlineformset_factory(
    Recipe, Step, form=StepForm, extra=1, can_delete=False,
)


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = '__all__'

        labels = {
            'name': _('Name'),
            'quantity': _('Quantity'),
            'measure': _('Measure'),
        }

    def __init__(self, *args, **kwargs):
        inline = kwargs.pop('inline', False)
        formset_form = kwargs.pop('formset_form', False)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        if formset_form:
            # In the context of formset, this is necessary because we need the
            # ID field.
            self.helper.render_hidden_fields = True

            # In a formset, this cannot be enforced anyway
            self.fields['name'].required = False

        if inline:
            self.helper.layout = Layout(
                Row(Column('name'), Column('quantity'), Column('measure'))
            )


RecipeIngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=False
)
