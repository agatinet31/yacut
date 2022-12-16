from datetime import datetime

from yacut import db
from yacut.utils import get_unique_short_id
from yacut.error_handlers import UniqueShortIDError


class YacutModel(db.Model):
    """Базовый класс модели."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]

    def to_dict(self):
        """Формирование словаря из объекта модели."""
        return dict(self)

    def from_dict(self, data):
        """Обновление полей модели из словаря."""
        self.__dict__.update(data)


class URLMap(YacutModel):
    """Класс модели отображения коротких ссылок."""
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


def append_urlmap(original, short=None):
    if not short:
        short = get_unique_short_id()
    if URLMap.query.filter_by(short=short).first():
        raise UniqueShortIDError
    urlmap = URLMap(
        original=original,
        short=short
    )
    db.session.add(urlmap)
    db.session.commit()
