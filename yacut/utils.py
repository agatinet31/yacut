from random import randrange

from sqlalchemy.exc import DatabaseError

from yacut import db
from yacut.error_handlers import UniqueShortIDError, YacutAppendUrlMapError
from yacut.models import URLMap

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


def append_urlmap(original, short=None):
    try:
        if not short:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first():
            raise UniqueShortIDError(short)
        urlmap = URLMap(
            original=original,
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        return urlmap
    except DatabaseError as exc:
        raise YacutAppendUrlMapError(original, short) from exc
