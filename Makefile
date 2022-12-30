setup: install lock

PORT ?= 8000

install:
	poetry install

lock:
	poetry lock

lint:
	poetry run flake8 page_analyzer

check:
	poetry check

test:
	poetry run pytest tests

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app
