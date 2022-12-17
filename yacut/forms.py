from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class UrlMapForm(FlaskForm):
    """Класс формы для ввода ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(1, 16, message='Длина короткого идентификатора не более 16 символов'),
            Regexp('[a-zA-Z0-9]+', message='Короткий идентификатор должен содержать только латинские буквы или цифры')
        ]
    )
    submit = SubmitField('Создать')
