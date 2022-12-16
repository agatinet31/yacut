from random import randrange

SHORT_CHAR_CODES = (
    (48, 58),
    (65, 91),
    (97, 123),
)


def get_unique_short_id():
    """Возвращает рандомный короткий идентификатор длиной 6 символов."""
    return ''.join([
        chr(randrange(*SHORT_CHAR_CODES[randrange(3)]))
        for _ in range(6)]
    )