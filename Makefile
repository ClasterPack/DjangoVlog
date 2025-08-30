# -------- Настройки (можно переопределить: make up DC="docker-compose") -------
DC ?= docker compose
FRONT_DIR ?= vue-frontend
CELERY_APP ?= DjangoVlog

# Параметры сидера (можно менять: make seed PAGES=50 MIN=5 MAX=15)
PAGES ?= 20
MIN ?= 5
MAX ?= 10

ID ?= 1

# ---------------------------------- Help --------------------------------------
.PHONY: help
help:
	@echo "Команды:"
	@echo "  make up                 - поднять все сервисы (build + up -d)"
	@echo "  make down               - остановить (без удаления volumes)"
	@echo "  make destroy            - остановить и удалить volumes"
	@echo "  make restart            - перезапустить web/worker/nginx"
	@echo "  make ps                 - статус контейнеров"
	@echo "  make logs               - логи всех сервисов"
	@echo "  make logs-web           - логи web"
	@echo "  make logs-worker        - логи worker"
	@echo "  make logs-nginx         - логи nginx"
	@echo "  make migrate            - применить миграции"
	@echo "  make makemigrations     - создать миграции"
	@echo "  make superuser          - создать суперпользователя"
	@echo "  make seed               - сгенерировать тестовые данные (PAGES=$(PAGES), MIN=$(MIN), MAX=$(MAX))"
	@echo "  make check ID=1         - сводка по странице (ID по умолчанию 1)"
	@echo "  make test               - запустить тесты"
	@echo "  make collectstatic      - собрать статику Django"
	@echo "  make web-sh             - шелл в web контейнере"
	@echo "  make worker-sh          - шелл в worker контейнере"
	@echo "  make celery-ping        - проверка доступности worker"
	@echo "  make frontend-install   - npm ci в $(FRONT_DIR)"
	@echo "  make frontend-build     - сборка Vue (vite build)"
	@echo "  make restart-nginx      - перезапуск nginx"
	@echo ""
	@echo "Подсказка: если у вас старая утилита, используйте DC='docker-compose'"

# -------------------------------- Docker --------------------------------------
.PHONY: up down destroy restart ps logs logs-web logs-worker logs-nginx
up:
	$(DC) up -d --build

down:
	$(DC) down

destroy:
	$(DC) down -v

restart:
	$(DC) restart web worker nginx

ps:
	$(DC) ps

logs:
	$(DC) logs -f

logs-web:
	$(DC) logs -f web

logs-worker:
	$(DC) logs -f worker

logs-nginx:
	$(DC) logs -f nginx

# ------------------------------- Django/DB -------------------------------------
.PHONY: migrate makemigrations superuser seed check test collectstatic
migrate:
	$(DC) exec web python manage.py migrate

makemigrations:
	$(DC) exec web python manage.py makemigrations

superuser:
	$(DC) exec web python manage.py createsuperuser

seed:
	$(DC) exec web python manage.py seed --pages $(PAGES) --min-per-page $(MIN) --max-per-page $(MAX)

check:
	$(DC) exec web python manage.py check_page $(ID)

test:
	$(DC) exec web python manage.py test -v 2

collectstatic:
	$(DC) exec web python manage.py collectstatic --noinput

# --------------------------------- Shell ---------------------------------------
.PHONY: web-sh worker-sh
web-sh:
	$(DC) exec web sh

worker-sh:
	$(DC) exec worker sh

# --------------------------------- Celery --------------------------------------
.PHONY: celery-ping
celery-ping:
	$(DC) exec worker celery -A $(CELERY_APP) inspect ping

# --------------------------------- Frontend ------------------------------------
.PHONY: frontend-install frontend-build restart-nginx
frontend-install:
	cd $(FRONT_DIR) && npm ci

frontend-build:
	cd $(FRONT_DIR) && npm run build

restart-nginx:
	$(DC) restart nginx