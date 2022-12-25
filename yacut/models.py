from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import synonym, validates
from sqlalchemy.orm.exc import NoResultFound

from yacut import app, db
from yacut.error_handlers import (UniqueShortIDError, YacutAppendUrlMapError,
                                  YacutDataBaseError, YacutValidationError)
from yacut.utils import get_obj_value, get_random_short_id
from yacut.validators import SHORT_ID_REGEX, URL_REGEX


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

    def to_dict(self, *keys):
        """Формирует словарь из объекта модели по ключевым атрибутам."""
        return dict(get_obj_value(self, *keys))

    def from_dict(self, **data):
        """Обновляет поля объекта модели из словаря."""
        for item in data.items():
            if hasattr(self, item[0]):
                self.__setattr__(*item)

    def save(self):
        """Сохраняет изменения в БД."""
        try:
            db.session.add(self)
            db.session.commit()
        except YacutDataBaseError:
            db.session.rollback()
            raise


class URLMap(YacutBaseModel):
    """Класс модели отображения коротких ссылок."""
    original = db.Column(
        db.String(256),
        index=True,
        nullable=False,
        default=''
    )
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    url = synonym('original')
    custom_id = synonym('short')
    short_link = synonym('short')
    length_short_key = app.config.get('LENGTH_SHORT_ID', 6)

    @validates('original')
    def validate_original(self, key, original):
        if not original:
            raise AssertionError('\"url\" является обязательным полем!')
        assert isinstance(original, str), 'Оригинальная ссылка - строка.'
        assert len(original) <= 256, (
            'Длина оригинальной ссылки не более 256 символов.'
        )
        if URL_REGEX.match(original) is None:
            raise ValueError(
                f'{original} Оригинальная ссылка не соответствует шаблону url адреса!'
            )
        return 'hren'

    @validates('short')
    def validate_short(self, key, short):
        assert isinstance(short, str), 'Короткая ссылка - строка.'
        assert len(short) <= 16, (
            'Длина короткой ссылки не более 16 симоволов.'
        )
        if SHORT_ID_REGEX.match(short) is None:
            raise ValueError('Указано недопустимое имя для короткой ссылки')
        return short

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
    def append_urlmap(cls, **data):
        """
        Добавление нового сопоставления
        между оригинальной ссылкой и коротким идентификатором.

        except IntegrityError as exc:
            # raise UniqueShortIDError(urlmap.short) from exc
            raise UniqueShortIDError(str(exc)) from exc

        """
        try:
            urlmap = cls()
            urlmap.from_dict(**data)
            if not urlmap.short:
                urlmap.short = cls.get_unique_short_id()
            urlmap.save()
            return urlmap
        except (AssertionError, ValueError) as exc:
            raise YacutValidationError(str(exc)) from exc
        except YacutDataBaseError as exc:
            raise YacutValidationError(str(exc)) from exc
            """
            raise YacutAppendUrlMapError(
                urlmap.original, urlmap.short
            ) from exc
            """

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return f'{self.short} : {self.original}'
