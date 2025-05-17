from django import template
import builtins  # to access the original zip

register = template.Library()

@register.filter(name='zip_lists')  # name must match template usage
def zip_lists(a, b):
    return builtins.zip(a, b)
