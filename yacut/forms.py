from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class OpinionForm(FlaskForm):
    """Класс формы для ввода ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(Length(1, 256), message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16, message='Длина короткого идентификатора не более 16 символов'),
            Optional(),
            Regexp(r'[a-zA-Z\d]+', message='Короткий идентификатор должен содержать только латинские буквы или цифры')
        ]
    )
    submit = SubmitField('Создать')
