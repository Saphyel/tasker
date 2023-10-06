FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV PATH="$PATH:/home/appuser/.local/bin"

ENV PORT 80
EXPOSE $PORT

WORKDIR /app

COPY pyproject.toml README.md ./

RUN pip install .

COPY tasker/ ./tasker/
COPY templates/ ./templates/

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app/
USER appuser

CMD uvicorn tasker.web:app --host 0.0.0.0 --port $PORT
