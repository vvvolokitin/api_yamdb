from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone

slug_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'разрешены символы латиницы, цифры, дефис и подчёркивание.'
)


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего.'
        )
