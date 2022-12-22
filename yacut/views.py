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
        urlmap = (
            URLMap.append_urlmap(
                form.original_link.data,
                form.custom_id.data
            ).short
            if form.validate_on_submit()
            else None
        )
    except UniqueShortIDError as exc:
        flash(str(exc))
    except YacutAppendUrlMapError:
        app.logger.exception(
            'Добавление нового сопоставления, '
            'введеного в форме сервиса не выполнено!'
        )
        abort(500)
    return render_template('yacut.html', form=form, urlmap=urlmap)


@app.route('/<custom_id>')
def redirect_view(custom_id):
    """View функция редиректа по оригинальной ссылке."""
    try:
        app.logger.info(f'short >>>>>   = {custom_id}')
        urlmap = URLMap.get_by_short(custom_id)
        app.logger.info(f'urlmap !!!!!!!!!!!!!!!!  = {urlmap}')
        return redirect(f'http://{urlmap.original}')
    except NoResultFound:
        abort(404)
    except YacutDataBaseError:
        app.logger.exception(
            'Ошибка редиректа при определении оригинальной ссылки '
            f'по короткому идентификатору {custom_id}!'
        )
        abort(500)
