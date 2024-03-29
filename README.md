# Проект YaCut — это сервис укорачивания ссылок. 
Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
Ключевые возможности сервиса:
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам.
Пользовательский интерфейс сервиса — одна страница с формой, состоящая из двух полей:
- обязательного для длинной исходной ссылки;
- необязательного для пользовательского варианта короткой ссылки.
Пользовательский вариант короткой ссылки не должен превышать 16 символов.
Если пользователь не заполнит поле со своим вариантом короткой ссылки, то сервис сгенерирует её автоматически. 
Формат для ссылки по умолчанию — шесть случайных символов:
- большие латинские буквы,
- маленькие латинские буквы,
- цифры в диапазоне от 0 до 9.
Автоматически сгенерированная короткая ссылка добавляться в базу данных.
## Использование
Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать и заполнить файл .env:
```
FLASK_APP=yacut
FLASK_ENV=production
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

Применить миграции:
```
flask db upgrade
```

Запустить сервис:
```
flask run
```

Страница сервиса будет доступна по адресу:
```
http://127.0.0.1:5000
```

### API для проекта
API проекта доступны всем желающим.
Сервис обслуживает только два эндпоинта:

/api/id/ — POST-запрос на создание новой короткой ссылки;
```
тело запроса:
{
  "url": "string",
  "custom_id": "string"
}
```
/api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.

### Документация API
В корне проекта расположен файл openapi.yml, содержащий описание работы с API сервиса.
Для удобной работы с документом воспользуйтесь онлайн-редактором Swagger Editor(https://editor.swagger.io/),
в котором можно визуализировать спецификацию.

## Автор
Андрей Лабутин