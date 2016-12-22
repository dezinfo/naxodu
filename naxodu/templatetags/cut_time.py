from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    test = value.split(delimiter)[0]
    v = test.split()
    r = v[0]+' '+v[1][:3]
    return r
upto.is_safe = True