from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from recipy.models import Recipe, Step
from model_bakery import baker


class ModelTests(TestCase):

    def test_recipe_get_duration_display_none(self):
        recipe = baker.make(Recipe)

        self.assertIsNone(recipe.duration_minutes)
        self.assertEqual('', recipe.get_duration_display())

    def test_recipe_get_duration_display_with_step_with_empty_duration(self):
        recipe = baker.make(Recipe)
        step = baker.make(Step, recipe=recipe)

        self.assertIsNone(recipe.duration_minutes)
        self.assertIsNone(step.duration_minutes)
        self.assertEqual('', recipe.get_duration_display())

    def test_recipe_get_duration_display_with_step(self):
        recipe = baker.make(Recipe)
        baker.make(Step, recipe=recipe, duration_minutes=1)

        self.assertIsNone(recipe.duration_minutes)
        self.assertEqual(f'1{_("min")}', recipe.get_duration_display())

    def test_recipe_get_duration_display_with_step_and_hour(self):
        recipe = baker.make(Recipe)
        baker.make(Step, recipe=recipe, duration_minutes=61)

        self.assertIsNone(recipe.duration_minutes)
        self.assertEqual(
            f'1{_("h")} 1{_("min")}', recipe.get_duration_display()
        )

    def test_step_get_duration_display_none(self):
        step = baker.make(Step)

        self.assertIsNone(step.duration_minutes)
        self.assertEqual('', step.get_duration_display())

    def test_step_get_duration_display(self):
        step = baker.make(Step, duration_minutes=1)
        self.assertEqual(f'1{_("min")}', step.get_duration_display())

    def test_step_get_duration_display_hours(self):
        step = baker.make(Step, duration_minutes=61)
        self.assertEqual(f'1{_("h")} 1{_("min")}', step.get_duration_display())
