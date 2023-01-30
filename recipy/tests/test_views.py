from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from recipy.models import Recipe, Step, Ingredient


def prepare_formset_data(prefix, parent_name, form_data_list,
                         initial_form_data_list=None):
    if initial_form_data_list is None:
        initial_form_data_list = []
    formset_data = {
        f'{prefix}-TOTAL_FORMS': len(form_data_list),
        f'{prefix}-INITIAL_FORMS': len(initial_form_data_list),
        f'{prefix}-MIN_NUM_FORMS': 0,
        f'{prefix}-MAX_NUM_FORMS': 1000,
    }

    for index, form_data in enumerate(initial_form_data_list):
        for field_name, value in form_data.items():
            key = f'{prefix}-{index}-{field_name}'
            formset_data[key] = value

    for index, form_data in enumerate(form_data_list):
        for field_name, value in form_data.items():
            # Skip ID fields and parent fields for new forms
            if field_name in ('id', parent_name):
                continue
            key = f'{prefix}-{index}-{field_name}'
            formset_data[key] = value

    return formset_data


def default_empty_string(value):
    return value if value else ''


class ViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        recipe = baker.make(Recipe)
        step = baker.make(Step, recipe=recipe)
        ingredient = baker.make(Ingredient, recipe=recipe)

        recipe_data = {
            'title': recipe.title,
            'description': default_empty_string(recipe.description),
            'duration_minutes': default_empty_string(recipe.duration_minutes),
        }

        step_data = {
            'recipe': recipe.pk,
            'id': step.pk,
            'name': step.name,
            'description': default_empty_string(step.description),
            'duration_minutes': default_empty_string(step.duration_minutes),
        }

        ingredient_data = {
            'recipe': recipe.pk,
            'id': ingredient.pk,
            'name': ingredient.name,
            'quantity': ingredient.quantity,
            'measure': default_empty_string(ingredient.measure),
        }

        cls.urls = {
            reverse('recipy:index'): {
                'get': {
                    'response_status_code': 302,
                    'redirects_to': reverse('recipy:recipes-list'),
                },
            },

            reverse('recipy:recipes-list'): {
                'get': {
                    'response_status_code': 200,
                },
            },

            reverse('recipy:recipe-create'): {
                'get': {
                    'response_status_code': 200,
                },
                'post': {
                    'response_status_code': 302,
                    'data': {
                        **recipe_data,
                        **prepare_formset_data('steps', 'recipe', [step_data]),
                        **prepare_formset_data(
                            'ingredients', 'recipe', [ingredient_data]
                        ),
                    },
                    'redirects_to': reverse('recipy:recipes-list'),
                },
            },

            reverse('recipy:recipe-update', args=(recipe.pk,)): {
                'get': {
                    'response_status_code': 200,
                },
                'post': {
                    'response_status_code': 302,
                    'data': {
                        **recipe_data,
                        **prepare_formset_data(
                            'steps', 'recipe', [],
                            initial_form_data_list=[step_data],
                        ),
                        **prepare_formset_data(
                            'ingredients', 'recipe', [],
                            initial_form_data_list=[ingredient_data],
                        ),
                    },
                    'redirects_to': reverse('recipy:recipes-list'),
                }
            },

            reverse('recipy:recipe-delete', args=(recipe.pk,)): {
                'post': {
                    'response_status_code': 302,
                    'data': {},
                    'redirects_to': reverse('recipy:recipes-list'),
                }
            },

            reverse('recipy:recipe-detail', args=(recipe.pk,)): {
                'get': {
                    'response_status_code': 200,
                }
            }
        }

    def test_urls(self):
        for url, url_test_conf in self.urls.items():
            with self.subTest(url=url):
                for method, method_test_conf in url_test_conf.items():
                    with self.subTest(method=method):
                        # Use transaction to isolate DB state between subtests
                        # This savepoint will be used for the rollback after.
                        savepoint = transaction.savepoint()

                        # Call the URL
                        response = getattr(self.client, method)(
                            url, data=method_test_conf.get('data')
                        )

                        # Check the status code
                        self.assertEqual(
                            response.status_code,
                            method_test_conf['response_status_code'],
                            msg=f'Response returned unexpected status code '
                                f'"{response.status_code}".'
                        )

                        # Check redirects if any
                        if 'redirects_to' in method_test_conf:
                            self.assertRedirects(
                                response, method_test_conf['redirects_to'],
                            )

                        # Rollback the DB to keep the tests isolated
                        transaction.savepoint_rollback(savepoint)
