from django.utils import timezone


def format_date(date_value):
    """Função para formatar as datas no formato DD/MM/YYYY"""
    if date_value:
        return date_value.strftime("%d/%m/%Y")
    return "-"


def format_datetime(datetime_value):
    """Função para formatar as datas no formato DD/MM/YYYY às hh:mm"""
    if datetime_value:
        # Se o datetime_value já está em UTC, converta para o horário local
        local_datetime = timezone.localtime(datetime_value)
        return local_datetime.strftime("%d/%m/%Y às %H:%M")
    return "-"
