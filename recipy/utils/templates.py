def get_id_for_model_instance(model_instance, action_prefix=''):
    model_name = model_instance._meta.model_name

    id_components = (model_name, str(model_instance.pk))
    if action_prefix:
        id_components = (action_prefix, *id_components)

    return '-'.join(id_components)
