from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, RedirectView, UpdateView

from recipy.forms import RecipeForm
from recipy.models import Recipe


class IndexView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('recipy:recipes-list')


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipy/recipe_list.html'


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipy/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form_title': _('Create recipe'),
            'form_submit_label': _('Create'),
        })

        return context

    def get_success_url(self):
        return reverse('recipy:recipes-list')


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipy/recipe_form.html'
    pk_url_kwarg = 'pk_recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form_title': _('Update recipe')})

        return context

    def get_success_url(self):
        return reverse('recipy:recipes-list')
