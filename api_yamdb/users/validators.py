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
