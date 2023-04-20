import re

from django.core.exceptions import ValidationError


def validate_username(username):
    """Валидация имени пользователя"""
    if not bool(re.match(r'^[\w.@+-]+$', username)):
        raise ValidationError(
            'Incorrect symbols in username.'
            'Use figures, letters and symbols: dot, @, +, -, _'
        )

    if username.lower() == 'me':
        raise ValidationError(
            'It is prohibited to set username as me'
        )
    return username


def validate_confirmation_code(confirmation_code):
    """Валидация кода подтверждения"""
    if not isinstance(confirmation_code, str):
        raise ValidationError('used not str')
    if len(confirmation_code) != 32:
        raise ValidationError('confirmation_code length != 32 symbols')
