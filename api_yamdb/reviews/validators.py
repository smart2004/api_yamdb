from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидация дат"""
    if value > timezone.now().year:
        raise ValidationError(
            ('Input year %(value)s greater than current year!'),
            params={'value': value},
        )


def validate_confirmation_code(confirmation_code):
    """Валидация кода подтверждения"""
    if not isinstance(confirmation_code, str):
        return True
    if len(confirmation_code) != 20:
        return True
    return False
