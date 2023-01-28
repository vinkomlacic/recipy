from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin


def get_id_for_model_instance(model_instance, action_prefix=''):
    model_name = model_instance._meta.model_name

    id_components = (model_name, str(model_instance.pk))
    if action_prefix:
        id_components = (action_prefix, *id_components)

    return '-'.join(id_components)


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
