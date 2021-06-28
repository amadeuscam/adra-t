from django import template
from adra.models import Alimentos

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    res = isinstance(instance, str)
    if res:
        return Alimentos._meta.get_field(field_name).verbose_name.title()
    else:
        return instance._meta.get_field(field_name).verbose_name.title()
