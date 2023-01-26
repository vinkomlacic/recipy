from django.views.generic import ListView

from recipy.models import Recipe


class RecipeListView(ListView):
    template_name = 'recipy/recipe_list.html'
    model = Recipe
    context_object_name = 'recipes'
