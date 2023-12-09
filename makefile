.PHONY: celery
celery:
	@poetry run celery -A app.celery_app worker --loglevel=INFO


.PHONY: serve
serve:
	@poetry run uvicorn app.main:app --reload


.PHONY: test
test:
	@poetry run pytest --verbose --capture=no
