from django.db import models
from django.utils.translation import gettext_lazy as _


def humanize_duration(duration_minutes: int) -> str:
    if duration_minutes > 60:
        hours, minutes = divmod(duration_minutes, 60)
        return f'{hours}{_("h")} {minutes}{_("min")}'
    else:
        return f'{duration_minutes}{_("min")}'


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    duration_minutes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_duration_display(self) -> str:
        """Returns a human readable duration."""
        if self.duration_minutes is None:
            # TODO: if duration is none try to collect it from the duration
            #  of the steps. If that amounts to nothing, only then return
            #  empty string.
            return ''

        return humanize_duration(self.duration_minutes)


class Ingredient(models.Model):

    class Measure(models.TextChoices):
        KG = 'KG', _('Kilogram')
        LITER = 'LITER', _('Liter')

    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    measure = models.CharField(max_length=255, choices=Measure.choices,
                               blank=True, null=True)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients')

    def __str__(self):
        return str(self.name)


class Step(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    duration_minutes = models.IntegerField(blank=True, null=True)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def get_duration_display(self) -> str:
        if self.duration_minutes is None:
            return ''

        return humanize_duration(self.duration_minutes)