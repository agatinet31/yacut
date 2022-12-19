from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Regexp


class UrlMapForm(FlaskForm):
    """Класс формы для ввода ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256, message='Длина ссылки не более 256 символов')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=16, message='Длина короткого идентификатора не более 16 символов'),
            Regexp(r'^[a-zA-Z\d]*$', message='Короткий идентификатор должен содержать только латинские буквы или цифры')
        ]
    )
    submit = SubmitField('Создать')
