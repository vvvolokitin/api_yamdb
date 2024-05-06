from django.core.validators import RegexValidator

slug_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'разрешены символы латиницы, цифры, дефис и подчёркивание.'
)
