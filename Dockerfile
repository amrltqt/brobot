FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ADD ./uv.lock ./pyproject.toml /app/
ADD ./brobot/ /app/brobot

RUN uv sync --locked

EXPOSE 8000
CMD ["/app/.venv/bin/fastapi", "run", "brobot/app.py", "--port", "8000", "--host", "0.0.0.0"]
