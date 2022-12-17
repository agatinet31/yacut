from datetime import datetime

from yacut import db


class YacutBaseModel(db.Model):
    """Базовый класс модели."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def __iter__(self):
        """Итератор полей и их значений."""
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


class URLMap(YacutBaseModel):
    """Класс модели отображения коротких ссылок."""
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
