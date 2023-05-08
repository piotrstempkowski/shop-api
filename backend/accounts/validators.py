import re

from django.core.validators import ValidationError


def polish_email_validator(email):
    pattern = r"^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9._%+-]+@[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9.-]+\.[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{2,}$"

    if not re.match(pattern, email):
        raise ValidationError("Wrong email input.")
