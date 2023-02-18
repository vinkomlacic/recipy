import abc
from enum import Enum

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin


class DirectDeleteView(SingleObjectMixin, DeletionMixin, View):
    """As opposed to regular DeleteView, this view does not have an
    intermediary deletion page. It simply deletes the object.

    In the templates, this can be used with render_delete_confirmation_modal
    and show_delete_confirmation_modal_btn tags from common_tags tag registry
    which show a confirmation modal screen instead of a special page.

    Usage:
        >>> class ObjectDeleteView(DirectDeleteView):
        >>>     model = Object
        >>>     pk_url_kwarg = 'pk_object'

    Template examples using suggested tags:
        >>> {% url 'object-delete' pk_object as form_action %}
        >>> {% render_delete_confirmation_modal object_instance form_action %}
        >>> {% show_delete_confirmation_modal_btn object_instance %}
    """
    pass


class DemoUserMixin:
    """
    Checks permissions for the Demo user.

    Possible options for `demo_user_permissions` tuple:
        - can_add_recipe

    Usage:
        >>> from recipy.utils.views import DemoUserMixin
        >>> from django.views.generic import CreateView
        >>> from django.contrib.auth.mixins import LoginRequiredMixin
        >>>
        >>> # Keep LoginRequiredMixin first. We need to check authentication
        >>> # before checking particular business logic permissions.
        >>> class AddView(LoginRequiredMixin, DemoUserMixin, CreateView):
        >>>     # ...
        >>>     demo_user_permissions = ('can_add_recipe',)
    """
    demo_user_permissions = None
    demo_user_redirect_to = reverse_lazy('recipy:recipes-list')

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self._validate_demo_user_permissions()

    def dispatch(self, *args, **kwargs):
        demo_user_permissions = self.get_demo_user_permissions()

        has_permission = True
        for permission in demo_user_permissions:
            # Each permission is a callable on this class
            has_permission &= getattr(self, permission)()

        if not has_permission:
            return redirect(self.demo_user_redirect_to)

        return super().dispatch(*args, **kwargs)

    def get_demo_user_permissions(self):
        if self.demo_user_permissions is None:
            msg = f'Please set demo_user_permissions attribute or override the '
            msg += f'get_demo_user_permissions method to use '
            msg += f'{DemoUserMixin.__name__}.'
            raise ImproperlyConfigured(msg)

        return self.demo_user_permissions

    def _validate_demo_user_permissions(self):
        demo_user_permissions = self.get_demo_user_permissions()
        valid_demo_user_permissions = ('can_add_recipe', )

        for permission in demo_user_permissions:
            if permission not in valid_demo_user_permissions:
                msg = f'Permission "{permission}" is not a valid '
                msg += f'demo_user_permission. Possible values are: '
                msg += f'{valid_demo_user_permissions}.'
                raise ImproperlyConfigured(msg)

    def can_add_recipe(self):
        if self._is_demo_user() and self._is_over_recipes_limit():
            recipe_limit = settings.RECIPY_DEMO_USER['recipe_limit']
            wmsg = f'Demo user can have no more than {recipe_limit} recipes. '
            wmsg += f'Also, keep in mind that the demo user data is deleted '
            wmsg += f'on daily basis. '
            messages.warning(self.request, wmsg)
            return False

        return True

    def _is_demo_user(self):
        user = self.request.user
        return user.username == settings.RECIPY_DEMO_USER['username']

    def _is_over_recipes_limit(self):
        user = self.request.user
        return user.recipes.count() >= settings.RECIPY_DEMO_USER['recipe_limit']


class RecipeAccessControlMixin(UserPassesTestMixin):
    """
    Implementation of access control policies for recipes.

    This mixin should be applied in combination with SingleObjectMixin.

    It implements the following policies:
        - All users need to be authenticated
        - All users are allowed to read public recipes
        - Only the users that are authors of the recipes are allowed to
            modify them
    """

    class Action(Enum):
        READ = 'read'
        MODIFY = 'modify'  # write or delete

    action: Action = None

    def get_action(self):
        if self.action is None:
            msg = f'"action" attribute needs to be set on the View when using '
            msg += f'{RecipeAccessControlMixin.__name__}. '
            raise ImproperlyConfigured(msg)

        return self.action

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        # Loading the object attribute here because the DetailView,
        # DeletionMixin, and UpdateView load it too late (in the dispatch
        # method).
        self.object = self.get_object()

    # This needs to be overridden because above the self.object is loaded early
    # and this is to cache the result so that it's not done twice.
    def get_object(self):
        if hasattr(self, 'object'):
            return self.object

        return super().get_object()

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False

        recipe = self.object
        action = self.get_action()
        if action == RecipeAccessControlMixin.Action.READ:
            if recipe.user != user and not recipe.is_public:
                return False
        elif action == RecipeAccessControlMixin.Action.MODIFY:
            if recipe.user != user:
                return False
        else:
            msg = f'"{action}" is not a supported action. '
            raise NotImplementedError(msg)

        return True
