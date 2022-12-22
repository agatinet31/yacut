from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from yacut import app, db
from yacut.error_handlers import (UniqueShortIDError, YacutAppendUrlMapError,
                                  YacutDataBaseError)
from yacut.utils import get_random_short_id


class YacutBaseModel(db.Model):
    """Базовый класс модели."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_one_or_error(cls, **filter):
        """Возвращает первую запись из применяемой выборки по фильтру."""
        return cls.query.filter_by(**filter).one()

    @classmethod
    def get_list_or_error(cls, **filter):
        """Возвращает список записей из применяемой выборки по фильтру."""
        records = cls.query.filter_by(**filter).all()
        if not records:
            raise NoResultFound
        return records

    def __iter__(self):
        """Итератор полей и их значений."""
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]

    def to_dict(self):
        """Формирует словарь из объекта модели."""
        return dict(self)

    def from_dict(self, data):
        """Обновляет поля модели из словаря."""
        self.__dict__.update(data)

    def save(self):
        """Сохраняет изменения в БД."""
        db.session.add(self)
        db.session.commit()


class URLMap(YacutBaseModel):
    """Класс модели отображения коротких ссылок."""
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    length_short_key = app.config.get('LENGTH_SHORT_ID', 6)

    @classmethod
    def get_by_short(cls, short):
        """Возвращает запись по короткому идентификатору."""
        return cls.get_one_or_error(short=short)

    @classmethod
    def get_by_original(cls, original):
        """Возвращает список записей по оригинальной ссылке."""
        return cls.get_list_or_error(original=original)

    @classmethod
    def is_short_exists(cls, short):
        """Проверка наличия короткого идентификатора."""
        try:
            return cls.get_by_short(short) is not None
        except NoResultFound:
            return False

    @classmethod
    def get_unique_short_id(cls):
        """Возвращает уникальный короткий идентификатор."""
        short_id = get_random_short_id(cls.length_short_key)
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
            if not short_id:
                short_id = cls.get_unique_short_id()
            urlmap = cls(
                original=original,
                short=short_id
            )
            urlmap.save()
            return urlmap
        except IntegrityError as exc:
            db.session.rollback()
            raise UniqueShortIDError(short_id) from exc
        except YacutDataBaseError as exc:
            raise YacutAppendUrlMapError(original, short_id) from exc

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return f'{self.short} : {self.original}'
