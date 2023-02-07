from django.contrib import admin
from accounts.models import RecipyUser


@admin.register(RecipyUser)
class DefaultAdmin(admin.ModelAdmin):
    pass
