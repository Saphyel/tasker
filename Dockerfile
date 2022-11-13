FROM python:3.10

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY pyproject.toml .

RUN pip install .
