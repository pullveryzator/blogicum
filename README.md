# Блокикум

**Блокикум** — это социальная сеть для публикации личных дневников. Пользователи могут создавать свои страницы, публиковать посты, выбирать категории и локации, а также читать и комментировать посты других пользователей.

## Основные возможности

- **Создание личной страницы**: Каждый пользователь может создать свою страницу и публиковать на ней посты.
- **Публикация постов**: Пользователи могут публиковать посты с указанием категории (например, "путешествия", "кулинария", "python-разработка") и опциональной локации (например, "Остров отчаянья", "Караганда").
- **Категории**: Пользователи могут перейти на страницу любой категории и увидеть все посты, которые к ней относятся.
- **Комментирование**: Пользователи могут читать и комментировать посты других пользователей.
- **Поиск и навигация**: Удобная навигация по категориям и локациям для быстрого поиска интересующих постов.

## Установка и запуск проекта

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/pullveryzator/django_sprint4.git
   cd django_sprint4
2. **Создайте и активируйте виртуальное окружение**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/MacOS
   venv\Scripts\activate     # Для Windows
4. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
6. **Примените миграции**:
   ```bash
   python manage.py migrate
8. **Создайте суперпользователя**:
   ```bash
   python manage.py createsuperuser
10. **Запустите сервер**:
    ```bash
   python manage.py runserver
12. **Откройте браузер и перейдите по адресу**:```bash
   http://127.0.0.1:8000/

## Тестирование

1. **Используйте следующую команду для запуска тестов**:
   ```bash
   pytest

## Структура проекта

- **Dev/**
  - **django_sprint4/**
    - `.vscode/` — служебная папка редактора кода (опционально, скрытая).
    - `.git/` — служебная информация Git (скрытая).
    - `tests/` — тесты, проверяющие проект.
    - `venv/` — директория виртуального окружения.
    - **blogicum/** — директория проекта.
      - `blog/` — приложение для управления постами и категориями.
      - `pages/` — приложение для статических страниц (например, "О проекте").
      - `static/` — статические файлы (CSS, JS, изображения).
      - `templates/` — HTML-шаблоны для отображения страниц.
      - **blogicum/** — основная конфигурация проекта (`settings.py`, `urls.py` и т.д.).
      - `db.sqlite3` — база данных SQLite (для разработки).
      - `manage.py` — скрипт для управления проектом.
    - `.gitignore` — список файлов и папок, скрытых от отслеживания Git.
    - `db.json` — фикстуры для базы данных.
    - `LICENSE` — лицензия проекта.
    - `pytest.ini` — конфигурация тестов.
    - `README.md` — описание проекта.
    - `requirements.txt` — список зависимостей проекта.
    - `setup.cfg` — настройки тестов.

## Используемые технологии

- **Django**: Основной фреймворк для разработки веб-приложения.

- **Django ORM**: Для работы с базой данных.

- **SQLite**: База данных для разработки.

- **HTML/CSS/JavaScript**: Для фронтенд-части проекта.

- **Bootstrap**: Для стилизации и адаптивного дизайна.

## Лицензия
- Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.

## Авторы
- https://github.com/pullveryzator
