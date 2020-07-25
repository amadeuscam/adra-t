import pickle

from django import template
register = template.Library()
import sys
import ast
from  ..models import Alimentos
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