from flask import abort, flash, redirect, render_template
from sqlalchemy.exc import DatabaseError

from yacut import app, db
from yacut.error_handlers import UniqueShortIDError
from yacut.forms import UrlMapForm
from yacut.models import URLMap, append_urlmap


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
    finally:
        return render_template('yacut.html', form=form)


@app.route('/<custom_id>')
def redirect_view(custom_id):
    """View функция редиректа по оригинальной ссылке."""
    urlmap = URLMap.query.filter_by(short=custom_id).first_or_404()
    return redirect(urlmap.original)
