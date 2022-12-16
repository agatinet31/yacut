from http import HTTPStatus

from flask import jsonify, render_template
from sqlalchemy.exc import DatabaseError

from yacut import app, db


class InvalidAPIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class UniqueShortIDError(Exception):

    def __init__(self, short_id):
        super().__init__(
            f'Имя {short_id} уже занято!'
        )
        self.short_id = short_id


@app.errorhandler(InvalidAPIError)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND.value


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR.value


@app.errorhandler(DatabaseError)
def database_error(error):
    app.logger.error(f'Ошибка работы с БД: {error}')
    return render_template('500.html'), 500