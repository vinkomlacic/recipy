from django.contrib import admin

from recipy.models import Recipe, Ingredient, Step


@admin.register(Recipe, Ingredient, Step)
class DefaultAdmin(admin.ModelAdmin):
    pass
