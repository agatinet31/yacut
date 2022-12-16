import csv

import click

from yacut import app, db
from yacut.models import URLMap


@app.cli.command('load_urlmap')
def load_urlmap():
    """Функция загрузки отображения коротких ссылок в базу данных."""
    with open('urlmap.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            urlmap = URLMap(**row)
            db.session.add(urlmap)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено коротких ссылок: {counter}')
