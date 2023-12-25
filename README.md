# Blogicum

**Blogicum** — это социальная сеть, где пользователи могут писать посты, публиковать их в различных категориях.

## Функции

- Позволяет пользователям создавать личные страницы и публиковать посты
- Посты могут иметь категории и опциональную локацию
- Другие пользователи могут просматривать страницы и комментировать посты
- Пользователи могут настраивать свои страницы и модерировать контент

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:andrew12022/foodgram-project-react.git
```

```
cd foodgram-project-react/backend
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Технологии и необходимые инструменты
- Python 3.9
- Django 3.2.16
- pytest
- sqlite3

## Автор
- [Андрей Елистратов](https://github.com/andrew12022)
