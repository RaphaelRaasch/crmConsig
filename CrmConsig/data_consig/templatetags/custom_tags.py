import locale
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django import template
from django.utils import timezone

from authentication.models import ROLE_CHOICES

register = template.Library()


@register.filter(name='format_cpf')
def format_cpf(value):
    if len(value) > 7 and isinstance(value, str):
        return f'{value[:3]}.{value[3:6]}.{value[6:9]}-{value[-2:]}'
    else:
        return value


@register.filter(name='age')
def age(value):
    return relativedelta(datetime.today().date(), value).years


@register.filter(name='currency')
def currency(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(value, grouping=True, symbol=None)


@register.filter(name='first_and_last_name')
def first_and_last_name(value):
    result = value.split()
    return f'{result[0]} {result[-1]}'


@register.filter(name='first_word')
def first_word(value):
    return value.split()[0]


@register.filter(name='is_real_time_and_updated')
def is_real_time_and_updated(matricula_detalhada):
    up_to_date = (timezone.now() - matricula_detalhada.updated_at).days
    if up_to_date < 60 and matricula_detalhada.real_time:
        return True


@register.filter(name='l_strip_zeros')
def l_strip_zeros(value):
    return str(value).lstrip('0')


@register.filter(name='role_text')
def role_text(value):
    choices = ROLE_CHOICES
    match_values = [x[1] for x in choices if x[0] == value]
    return match_values[0] if match_values else value


@register.filter(name='account_type')
def account_type(value):
    if value == 'CONTA CORRENTE':
        return 'C/C', 'CORRENTE'
    elif value == 'CONTA POUPANÇA':
        return 'C/P', 'POUPANÇA'
    elif value == 'CARTÃO MAGNÉTICO':
        return 'C/M', 'MAGNÉTICO'
    else:
        return [None, None]
