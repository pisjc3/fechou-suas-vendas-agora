from django.core.exceptions import ValidationError
import re


def telefone_validator(value):
    telefone_pattern = re.compile(
        r'^\(\d{2}\) \d{5}-\d{4}$')  # Máscara (99) 99999-9999
    if not telefone_pattern.match(value):
        raise ValidationError(
            'Número de telefone inválido. Use o formato (99) 99999-9999.')


def cnpj_validator(cnpj):
    # Remove caracteres não numéricos
    cnpj = re.sub(r'[^0-9]', '', cnpj)

    if len(cnpj) != 14:
        return False

    # Valida os CNPJ com números repetidos (ex: 11111111111111)
    if cnpj == cnpj[0] * len(cnpj):
        return False

    # Validação dos dois dígitos verificadores
    def calcular_digitos(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
        digito = 11 - (soma % 11)
        return digito if digito < 10 else 0

    # Pesos para o primeiro e segundo dígito verificador
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    # Calcula o primeiro e segundo dígito verificador
    digito_1 = calcular_digitos(cnpj, pesos_1)
    digito_2 = calcular_digitos(cnpj, pesos_2)

    return cnpj[-2:] == f"{digito_1}{digito_2}"
