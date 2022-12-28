setup: prepare install lock

install:
	poetry install

lock:
	poetry lock

lint:
	poetry run flake8 page_analyzer

prepare:
	cp -n .env.example .env

check:
	poetry check

test:
	poetry run pytest tests

test-coverage:
	poetry run pytest --cov=. --cov-report xml tests

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 3 -b 0.0.0.0:5000 page_analyzer:app