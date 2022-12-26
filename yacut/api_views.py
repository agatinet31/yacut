from http import HTTPStatus

from flask import jsonify, request
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from yacut import app
from yacut.error_handlers import (InvalidAPIError, UniqueShortIDError,
                                  YacutDataBaseError, YacutValidationError)
from yacut.models import URLMap


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url_map(short_id):
    """
    Возвращает оригинальную ссылку по короткому идетификатору.
    """
    try:
        urlmap = URLMap.get_by_short(short_id)
        return jsonify(urlmap.to_dict('url')), HTTPStatus.OK.value
    except NoResultFound:
        raise InvalidAPIError('Указанный id не найден', HTTPStatus.NOT_FOUND.value)
    except YacutDataBaseError:
        error_message = (
            'Внутреняя ошибка сервиса при определении оригинальной ссылки '
            f'по короткому идентификатору {short_id}!'
        )
        app.logger.exception(error_message)
        raise InvalidAPIError(error_message, HTTPStatus.INTERNAL_SERVER_ERROR.value)


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    """
    Создание отображения между оригинальной ссылкой и коротким идентификатором.
    """
    try:
        data = request.get_json()
        assert data is not None
        assert isinstance(data, dict)
        urlmap = URLMap.append_urlmap(**data)
        return (
            jsonify(urlmap.to_dict('url', 'short_link')),
            HTTPStatus.CREATED.value
        )
    except (AssertionError, BadRequest):
        raise InvalidAPIError('Отсутствует тело запроса')
    except (YacutValidationError, UniqueShortIDError) as exc:
        raise InvalidAPIError(str(exc))
    except YacutDataBaseError:
        error_message = (
            'Внутреняя ошибка сервиса при создании отображения между '
            f'оригинальной ссылкой {data.get("url")} и коротким идентификатором'
        )
        app.logger.exception(error_message)
        raise InvalidAPIError(error_message, HTTPStatus.INTERNAL_SERVER_ERROR.value)
