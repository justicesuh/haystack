FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /usr/app

RUN apt update && apt install -y firefox-esr wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.36.0-linux64.tar.gz
RUN chmod +x geckodriver && mv geckodriver /usr/local/bin/geckodriver
RUN rm geckodriver-v0.36.0-linux64.tar.gz

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked
COPY . .

CMD /bin/bash
