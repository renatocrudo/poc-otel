FROM python:3.12.2-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/

RUN pip install poetry

COPY pyproject.toml .

RUN poetry install

RUN pip install opentelemetry-distro

RUN opentelemetry-bootstrap -a install

COPY . .

CMD opentelemetry-instrument \
    uvicorn samba.app:app \
    --port 8001 \
    --host 0.0.0.0