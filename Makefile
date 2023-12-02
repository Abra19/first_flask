install:
	poetry install

lint:
	poetry run flake8 first_flask

start_dev:
	poetry run flask --app first_flask.service --debug run --port 8001

start_prod:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8001 first_flask.service:app

