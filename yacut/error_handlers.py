from http import HTTPStatus

from flask import jsonify, render_template
from sqlalchemy.exc import DatabaseError as YacutDataBaseError

from yacut import app


class InvalidAPIError(Exception):
    """Класс обработки исключений при обработке API."""
    status_code = HTTPStatus.BAD_REQUEST.value

    def __init__(self, message, status_code=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__()

    def to_dict(self):
        return dict(message=self.message)


class UniqueShortIDError(Exception):
    """Класс исключения уникальности для короткого идентификатора."""
    def __init__(self, short_id):
        self.short_id = short_id
        super().__init__(
            f'Имя {short_id} уже занято!'
        )


class YacutAppendUrlMapError(YacutDataBaseError):
    """
    Класс исключения для операции добавления в БД
    сопоставления оригинального URL и короткого идентификатора.
    """
    def __init__(self, original, short):
        self.original = original
        self.short = short
        super().__init__(
            'Ошибка при работа с БД. '
            'Операция добавления короткой ссылки не выполнена! '
            f'Оригинальная ссылка: {original} '
            f'Короткий идентификатор: {short}',
            self.orig,
            self.params
        )


@app.errorhandler(InvalidAPIError)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND.value)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND.value


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
def internal_error(error):
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR.value
