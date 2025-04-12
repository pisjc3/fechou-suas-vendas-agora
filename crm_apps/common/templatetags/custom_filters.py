from django import template
from crm_apps.common.util.formats import format_currency
register = template.Library()


@register.filter(name="get_param")
def get_param(request_get, param_name):
    if isinstance(request_get, dict):
        return request_get.get(param_name, '')
    return ''


@register.filter
def currency(value):
    return format_currency(value)
