PDF text extraction service using Fastapi for the backend, Celery for the task queue and Preact for the frontend.

Install the dependencies:
```sh
poetry install
```

Create .env file:
```sh
cp .env_template .env
```
Add celery [broker and backend](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html) into .env file. For example
```
celery_backend="redis://127.0.0.1:6379/0"
celery_broker="redis://127.0.0.1:6379/0"
```

Start the Celery worker:
```sh
make celery
```

Start the FastAPI server:
```sh
make serve
```

Run tests
```sh
make test
```

Tags: python, pdf, fastapi, celery,  preact
