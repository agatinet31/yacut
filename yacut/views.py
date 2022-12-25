from http import HTTPStatus

from flask import abort, flash, redirect, render_template
from sqlalchemy.orm.exc import NoResultFound

from yacut import app
from yacut.error_handlers import (UniqueShortIDError, YacutAppendUrlMapError,
                                  YacutDataBaseError)
from yacut.forms import UrlMapForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View функция главной страницы."""
    try:
        form = UrlMapForm()
        urlmap = None
        if form.validate_on_submit():
            urlmap = URLMap.append_urlmap(
                original=form.original_link.data,
                short=form.custom_id.data
            )
    except UniqueShortIDError as exc:
        flash(str(exc))
    except YacutAppendUrlMapError:
        app.logger.exception(
            'Добавление нового сопоставления, '
            'введеного в форме сервиса не выполнено!'
        )
        abort(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    return render_template('yacut.html', form=form, urlmap=urlmap)


@app.route('/<custom_id>')
def redirect_view(custom_id):
    """View функция редиректа по оригинальной ссылке."""
    try:
        urlmap = URLMap.get_by_short(custom_id)
        return redirect(urlmap.original)
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND.value)
    except YacutDataBaseError:
        app.logger.exception(
            'Ошибка редиректа при определении оригинальной ссылки '
            f'по короткому идентификатору {custom_id}!'
        )
        abort(HTTPStatus.INTERNAL_SERVER_ERROR.value)
