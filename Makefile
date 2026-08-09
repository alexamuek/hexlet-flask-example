build:
	./build.sh

prod:
	uv run gunicorn --workers=4 --bind=127.0.0.1:8000 example4:app
dev:
	uv run flask --app example4 run --port 8000 --debug
install:
	uv sync