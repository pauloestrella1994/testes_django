test:
	poetry run python sorveteria/manage.py test

makemigrations:
	poetry run python sorveteria/manage.py makemigrations

migrate:
	poetry run python sorveteria/manage.py migrate

env:
	cp local.env .env

