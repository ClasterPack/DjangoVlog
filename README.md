## <p align="center">DjangoVlog — CMS API + Vue SPA</p>
## Описание:
 Проект демонстрирует бэкенд на Django/DRF с контентом разных типов (видео, аудио), API со списком страниц и детальными данными, фоновый атомарный инкремент счетчиков просмотров через Celery, кэширование в Redis, админку с инлайнами и поиск по заголовкам. Фронтенд — Vue 3 (Vite), собирается в статический билд и обслуживается Nginx с корня, а API и админка проксируются на Django по /api и /admin.

## Стек
* Backend: Django 4, Django REST Framework, Celery, Redis, PostgreSQL
* Frontend: Vue 3 (Vite)
* Web: Nginx (SPA с корня, API под /api)
* Контейнеризация: Docker Compose
* Кэш: django-redis (Redis)
* Документация API: drf-spectacular (Swagger UI, Redoc)

## Функционал

API страниц:

`GET` `/api/pages/` — список страниц с пагинацией и detail_url на детальный эндпоинт

`GET` `/api/pages/{id}/` — детальная информация: атрибуты страницы + упорядоченный вложенный список контента (видео/аудио), включая специфичные поля
### Счетчики просмотров:
При запросе деталей страницы все привязанные объекты контента получают +1 просмотр
Инкремент выполняется в фоне (Celery), атомарно (через F-выражения), корректно при параллелизме
### Кэширование:
Детальный ответ страницы кэшируется в Redis (TTL настраивается), инвалидация по сигналам при изменении связей/контента
### Админка:
Read-only поле counter в моделях контента
Inline PageContent на форме Page с отображением связанного объекта и его counter
Поиск по title (истартсвыш)
### OpenAPI:
Схема и UI по /api/schema, /api/docs (Swagger), /api/redoc (Redoc)
### Тесты:
Позитивные тесты списка и деталей с проверкой инкремента (в eager-режиме Celery)
### Генерация данных:
management-команды для сидирования тестовой БД и проверки страницы
### Основные директории
* app — Django приложение (модели, сериализаторы, вью, задачи Celery, сигналы, комманды)
* DjangoVlog — конфигурация проекта (settings, celery, urls)
* vue-frontend — фронтенд Vue 3 (Vite) — исходники и сборка
* nginx — конфиг nginx (SPA с корня, API и admin проксируются)
* docker-compose.yml — сервисы: db (Postgres), redis, web (Django), worker (Celery), nginx
* docker-entrypoint.sh — миграции, collectstatic, запуск сервера
* requirements.txt — зависимости Python
* Makefile — частые команды (обертки над docker compose)
* .env.example — пример переменных окружения (на основе pydantic-settings)
Переменные окружения (пример .env)
Не коммитить .env в репозиторий — используйте .env.example как шаблон.
## Быстрый старт (Docker)
### Создайте .env из примера:
`cp .env.example .env`
### Соберите фронтенд (на хосте должен быть NodeJS):
* `make frontend-install`
* `make frontend-build`
### Поднимите стек:
* `make up`
### Примените миграции и создайте суперпользователя:
* `make migrate`
* `make superuser`
### (Опционально) заполните БД тестовыми данными:
* `make seed`
* Параметры сидера можно задать так: `make seed PAGES=50 MIN=10 MAX=20`
### URL по умолчанию
* Корень SPA (Vue): http://localhost/
* Список страниц (JSON): http://localhost/api/pages/
* Детали страницы (JSON): http://localhost/api/pages/1/
* Админка: http://localhost/admin/
* Swagger UI: http://localhost/api/docs/
* Redoc: http://localhost/api/redoc/

### Как это работает

Детальный эндпоинт страницы извлекает связанные объекты контента (Video/Audio) в порядке position и сериализует их вместе со специфичными полями. Результат кэшируется в Redis на PAGE_DETAIL_CACHE_TTL секунд. Кэш инвалидируется сигналами при изменении связей (PageContent) и при сохранении/удалении самих объектов контента (Video/Audio).
После отдачи ответа ставится Celery-задача increment_counters с батчем объектов. Обновление выполняется атомарно на уровне SQL (UPDATE ... SET counter = counter + N). При недоступности брокера предусмотрен фолбэк на синхронный инкремент.
Из-за фонового характера инкремента и кэширования цифры counter в JSON могут отставать до TTL. Для проверки роста счетчиков используйте команду проверки или обновите страницу с деталями через секунду.
## Полезные команды (Makefile)
* `make up` — собрать и поднять сервисы (build + up -d)
* `make down` — остановить
* `make destroy` — остановить и удалить volumes
* `make restart` — перезапустить web/worker/nginx
* `make ps` — статус контейнеров
* `make logs`, `logs-web`, `logs-worker`, `logs-nginx` — логи
* `make migrate` — применить миграции
* `make makemigrations` — создать миграции
* `make superuser` — создать суперпользователя
* `make seed` — сгенерировать данные (по умолчанию 20 страниц, по 5–10 объектов)
* `make check ID=1` — сводка по странице
* `make test` — запустить тесты Django
* `make collectstatic` — собрать статику
* `make web-sh, worker-sh` — shell в контейнерах
* `make celery-ping` — проверить доступность Celery
* `make frontend-install` — npm ci во фронте
* `make frontend-build` — vite build
* `make restart-nginx` — перезапустить nginx
### Сидирование и проверка (management-команды)
Создание тестовых данных:
docker compose exec web python manage.py seed --pages 100 --min-per-page 10 --max-per-page 20
Сводка по странице:
docker compose exec web python manage.py check_page 1 --show 15
### Фронтенд (Vue)
Исходники в директории vue-frontend. Сборка выполняется через npm run build, результат попадает в vue-frontend/dist. В docker-compose папка dist примонтирована в nginx по /usr/share/nginx/html, поэтому SPA отдается с корня /. Все запросы к API должны идти на префикс /api, чтобы не было CORS и чтобы Nginx корректно проксировал на Django.
### Точки интеграции
В Nginx:
Корень / — статический билд Vue (dist)
Прокси /api/ и /admin/ — на Django web:8000
Папка /static/ — статические файлы Django (STATIC_ROOT)
### В Django:
INSTALLED_APPS — app.apps.AppConfig, DRF, drf-spectacular, django.contrib.postgres
Celery конфигурация в DjangoVlog/celery.py
Redis-кэш через django-redis (CACHE_URL)
Сигналы подключены в app.apps.AppConfig.ready()
### Тесты
Тесты лежат в app/tests.py. Запуск:
`make test`
или
`docker compose exec web python manage.py test -v 2`
### Отладка и советы
* Если на корне открывается не SPA, проверьте nginx.conf и что vue-frontend/dist создан (npm run build) и примонтирован в контейнер.
* Если счетчики не растут — проверьте, что Celery worker видит Redis (логи worker). Для мгновенной проверки можно установить CELERY_TASK_ALWAYS_EAGER=True в .env и перезапустить.
* Если `/api/pages/` пустой — засеять БД командой seed.
* Если `Invalid Host header` — проверьте ALLOWED_HOSTS в .env.
* В Linux пути чувствительны к регистру. Убедитесь, что файл `app/cache_keys.py` назван корректно и импорты соответствуют.
### Локальный запуск без Docker (опционально)
#### Установить Postgres и Redis локально. Настроить .env на localhost.
#### Установить зависимости Python:
`pip install -r requirements.txt`
#### Применить миграции и запустить:
`python manage.py migrate
python manage.py runserver`
#### Запустить Celery worker:
`celery -A DjangoVlog worker -l info`
#### Собрать фронтенд (либо запустить dev-сервер Vite):
`cd vue-frontend && npm ci && npm run build`
#### В прод-режиме лучше обслуживать сборку через nginx (как в compose).