from random import choices as random_choices
from string import ascii_letters, digits

ALPHABET = ascii_letters + digits


def get_random_short_id(length_short_id: int) -> str:
    """
    Возвращает рандомный короткий идентификатор
    длиной length_short_id символов.
    """
    return ''.join(random_choices(ALPHABET, k=length_short_id))
