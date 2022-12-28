install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest tests

test-coverage:
	poetry run pytest --cov=. --cov-report xml tests

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 3 -b 0.0.0.0:5000 page_analyzer:app