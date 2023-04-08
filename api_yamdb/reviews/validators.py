import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Input year %(value)s greater than current year!'),
            params={'value': value},
        )
    
def validate_username(username):
    if not bool(re.match(r'^[\w.@+-]+$', username)):
#    if not bool(re.match(r'^[\w.@+-]+\z', username)):
        raise ValidationError(
            'Incorrect symbols in username.'
            'Use figures, letters and symbols: dot, @, +, -, _'
        )

    if username.lower() == 'me':
        raise ValidationError(
            'It is prohibited to set username as me'
        )
    return username