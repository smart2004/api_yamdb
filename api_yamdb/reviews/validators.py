from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидация дат"""
    if value > timezone.now().year:
        raise ValidationError(
            ('Input year %(value)s greater than current year!'),
            params={'value': value},
        )

