from django import template
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from recipy.utils.templates import get_id_for_model_instance

register = template.Library()


@register.simple_tag
def setting(setting_name):
    return getattr(settings, setting_name, '')


@register.inclusion_tag('recipy/modal.html')
def render_modal(model_instance, **kwargs):
    """Renders a modal (hidden) for a model instance.

    Args:
        model_instance: instance of some model on which the operation is
            taking place

    Keyword Args:
        form_action: this is the URL that gets triggered when modal submit
            button is clicked. Modal submission submits a form. This form is
            by default empty (only contains CSRF field), but you can override
            it using form kwarg.
        action_prefix: used in building the modal HTML id. If you have
            multiple modals for the same model instance, this should be used
            to differentiate the modals. By default, empty string.
        form: set this if you want to override the default empty form to
            include more fields
        modal_title: by default, model verbose name
        modal_text: text displayed in the modal body
        submit_btn_color: color class of the submit button. The available
            values are danger, primary, secondary, ... - all that comes in the
            btn-* css class. By default, primary color class is used.
        submit_btn_text: by default "OK"
        submit_btn_disabled: disabled the submit button. By default, False.
        extra_modal_classes: HTML classes that will be added to the main
            modal div
    """
    model_verbose_name = model_instance._meta.verbose_name

    # Set default values
    action_prefix = kwargs.setdefault('action_prefix', '')
    kwargs.setdefault('modal_title', model_verbose_name)
    kwargs.setdefault('submit_btn_color', 'primary')
    kwargs.setdefault('submit_btn_text', _('OK'))
    kwargs.setdefault('submit_btn_disabled', False)

    # Set required values
    modal_id = get_id_for_model_instance(model_instance, action_prefix)
    kwargs.update(modal_id=modal_id)

    return kwargs


@register.inclusion_tag('recipy/modal_btn.html')
def show_modal_btn(model_instance, **kwargs):
    """Shows a button which displays the modal. You need to render the modal
    somewhere in order to be able to use this button.

    Args:
        model_instance: model_instance: instance of some model on which the
            operation is taking place

    Keyword Args:
        action_prefix: used in building the modal HTML id. If you have
            multiple modals for the same model instance, this should be used
            to differentiate the modals. By default, empty string.
        btn_small: if True 'btn-sm' CSS class will be used. True by default.
        btn_color: color class of the button accepts all btn-* color classes.
            By default, 'primary'.
        btn_fa_icon_class: if set, an icon will be displayed in the beginning
            of the button. Accepts all fa-* classes. You don't need to
            add a 'fa' class before.
        btn_text: text of the button. Empty by default
        btn_classes: classes that will be added on the button (<a>)
            element. By default, 'btn'.
        btn_element: button HTML attribute, by default 'a' (<a>)
    """
    # Set default values
    action_prefix = kwargs.setdefault('action_prefix', '')
    btn_small = kwargs.setdefault('btn_small', True)
    btn_color = kwargs.setdefault('btn_color', 'primary')
    kwargs.setdefault('btn_text', '')

    # Sometimes, <a> has left margin of 5, so we remove that. Also, sometimes,
    # the text is gray instead of white so we force white text.
    btn_classes = f'btn btn-{btn_color} ml-0 text-white '
    if btn_small:
        btn_classes += 'btn-sm '
    kwargs.setdefault('btn_classes', btn_classes)
    kwargs.setdefault('btn_element', 'a')

    # Set required values
    modal_id = get_id_for_model_instance(model_instance, action_prefix)
    kwargs.update(modal_id=modal_id)

    return kwargs


@register.inclusion_tag('recipy/modal.html')
def render_delete_confirmation_modal(model_instance, form_action):
    modal_title = \
        _('Are you sure you want to delete this %(model_name)s?') % \
        {'model_name': model_instance._meta.verbose_name}

    return render_modal(
        model_instance, form_action=form_action, action_prefix='confirm-delete',
        modal_title=modal_title,
        modal_text=_('Deleting is a permanent action. Are you sure?'),
        submit_btn_color='danger', submit_btn_text=_('Delete'),
    )


@register.inclusion_tag('recipy/modal_btn.html')
def show_delete_confirmation_modal_btn(model_instance, btn_text=''):
    return show_modal_btn(
        model_instance, action_prefix='confirm-delete',
        btn_text=btn_text, btn_color='danger',
        btn_fa_icon_class='fa-trash'
    )


@register.simple_tag
def element_id(element_name):
    elements = {
        'logout-modal': 'logout-modal',
    }

    return elements[element_name]


@register.inclusion_tag('recipy/formset.html')
def show_formset(formset, model, add_more_btn_text=None,
                 is_dynamic_formset=False):
    return {
        'formset_id': get_id_for_model_instance(model),
        'formset': formset,
        'add_more_btn_text': add_more_btn_text,
        'is_dynamic_formset': is_dynamic_formset,
    }


@register.inclusion_tag('recipy/formset_empty_form.html')
def render_formset_empty_form(formset, model):
    return {
        'formset_id': get_id_for_model_instance(model),
        'formset': formset,
    }
