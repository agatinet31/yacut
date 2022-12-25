from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Regexp

from yacut.validators import SHORT_ID_REGEX, URL_REGEX


class UrlMapForm(FlaskForm):
    """Класс формы для ввода ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(
                min=1,
                max=256,
                message='Длина ссылки не более 256 символов'
            ),
            Regexp(
                URL_REGEX,
                message='Поле должно содержать URL адрес'
            )
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                max=16,
                message='Длина короткого идентификатора не более 16 символов'
            ),
            Regexp(
                SHORT_ID_REGEX,
                message='Короткий идентификатор должен содержать только латинские буквы или цифры'
            )
        ]
    )
    submit = SubmitField('Создать')
