from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    ListView, CreateView, RedirectView, UpdateView, DetailView
)

from recipy.forms import RecipeForm
from recipy.models import Recipe
from recipy.utils.views import (
    DirectDeleteView, DemoUserMixin, RecipeAccessControlMixin
)


class IndexView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('recipy:recipes-list')


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipy/recipe_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(user=self.request.user) | Q(is_public=True))
        return qs

    def get_context_data(self, *args, **kwargs):
        public_recipes = self.object_list.filter(is_public=True).exclude(
            user=self.request.user
        )
        user_recipes = self.object_list.filter(user=self.request.user)

        return super().get_context_data(
            *args, public_recipes=public_recipes, user_recipes=user_recipes,
            **kwargs
        )


class RecipeCreateView(LoginRequiredMixin, DemoUserMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipy/recipe_form.html'
    demo_user_permissions = ('can_add_recipe',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form_title': _('Create recipe'),
            'form_submit_label': _('Create'),
        })

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('recipy:recipes-list')


class RecipeUpdateView(RecipeAccessControlMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipy/recipe_form.html'
    pk_url_kwarg = 'pk_recipe'
    action = RecipeAccessControlMixin.Action.MODIFY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form_title': _('Update recipe')})

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('recipy:recipes-list')


class RecipeDeleteView(RecipeAccessControlMixin, DirectDeleteView):
    model = Recipe
    pk_url_kwarg = 'pk_recipe'
    action = RecipeAccessControlMixin.Action.MODIFY

    def get_success_url(self):
        return reverse('recipy:recipes-list')


class RecipeDetailView(RecipeAccessControlMixin, DetailView):
    model = Recipe
    pk_url_kwarg = 'pk_recipe'
    template_name = 'recipy/recipe_detail.html'
    context_object_name = 'recipe'
    action = RecipeAccessControlMixin.Action.READ
