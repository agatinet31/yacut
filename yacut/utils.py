from random import choices as random_choices
from string import ascii_letters, digits
from typing import Any, Tuple

ALPHABET = ascii_letters + digits


def get_random_short_id(length_short_id: int) -> str:
    """
    Возвращает рандомный короткий идентификатор
    длиной length_short_id символов.
    """
    return ''.join(random_choices(ALPHABET, k=length_short_id))


def get_obj_value(obj: Any, *keys: str) -> Tuple[str, Any]:
    """Генератор наименования и значений атрибутов объекта по списку ключей."""
    tuple
    for name in keys:
        try:
            yield name, getattr(obj, name)
        except AttributeError:
            continue
