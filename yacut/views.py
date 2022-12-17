from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.error_handlers import (UniqueShortIDError, YacutAppendUrlMapError,
                                  YacutDataBaseError)
from yacut.forms import UrlMapForm
from yacut.models import URLMap
from yacut.utils import append_urlmap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View функция главной страницы."""
    try:
        form = UrlMapForm()
        if form.validate_on_submit():
            append_urlmap(
                form.original_link.data,
                form.custom_id.data
            )
    except UniqueShortIDError as exc:
        flash(exc)
    except YacutAppendUrlMapError:
        app.logger.exception(
            'Добавление нового сопоставления '
            'введеного в форме сервиса не выполнено!'
        )
        abort(500)
    return render_template('yacut.html', form=form)


@app.route('/<custom_id>')
def redirect_view(custom_id):
    """View функция редиректа по оригинальной ссылке."""
    try:
        urlmap = URLMap.query.filter_by(short=custom_id).first_or_404()
        return redirect(urlmap.original)
    except YacutDataBaseError:
        app.logger.exception(
            'Ошибка редиректа при определении оригинальной ссылки '
            f'по короткому идентификатору {custom_id}!'
        )
        abort(500)
