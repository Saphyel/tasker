FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV PORT 80
EXPOSE $PORT

WORKDIR /app

COPY pyproject.toml /app/

RUN pip install .

COPY . /app

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
