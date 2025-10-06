FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/app

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked
COPY . .

CMD /bin/bash
