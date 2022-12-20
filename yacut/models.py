from datetime import datetime

from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.exc import NoResultFound

from yacut import db
from yacut.error_handlers import UniqueShortIDError, YacutAppendUrlMapError
from yacut.utils import get_random_short_id


class YacutBaseModel(db.Model):
    """Базовый класс модели."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        """Возвращает объект по идентификатору."""
        return cls.query.filter_by(id=id).one()

    @classmethod
    def get_records_by_filter(cls, **filter):
        """Применяет фильтр к набору данных."""
        urlmaps = cls.query.filter_by(**filter)
        if not urlmaps:
            raise NoResultFound
        return urlmaps

    def save(self):
        """Сохраняет изменения в БД."""
        db.session.add(self)
        db.session.commit()

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

    @classmethod
    def get_by_short(cls, short):
        """Возвращает запись по короткому идентификатору."""
        return cls.get_records_by_filter(short=short).first()

    @classmethod
    def get_by_original(cls, original):
        """Возвращает список записей по оригинальной ссылке."""
        return cls.get_records_by_filter(original=original).all()

    @classmethod
    def is_short_exists(cls, short):
        """Проверка наличия короткого идентификатора в таблице."""
        return cls.get_by_short(short) is not None

    @classmethod
    def get_unique_short_id(cls):
        """Возвращает уникальный короткий идентификатор длиной 6 символов."""
        short_id = get_random_short_id(6)
        return (
            short_id
            if not cls.is_short_exists(short_id)
            else cls.get_unique_short_id()
        )

    @classmethod
    def append_urlmap(cls, original, short_id=None):
        """
        Добавление нового сопоставления
        между оригинальной ссылкой и коротким идентификатором.
        """
        try:
            if short_id is None:
                short_id = cls.get_unique_short_id()
            elif cls.is_short_exists(short_id):
                raise UniqueShortIDError(short_id)
            urlmap = cls(
                original=original,
                short=short_id
            )
            urlmap.save()
            return urlmap
        except DatabaseError as exc:
            raise YacutAppendUrlMapError(original, short_id) from exc

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return f'{self.short} : {self.original}'
