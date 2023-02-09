from django import template


register = template.Library()


@register.filter
def is_current_url(url: str, request):
    return url in request.path
