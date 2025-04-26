FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD pyproject.toml /app/pyproject.toml
ADD ./brobot /app/brobot
ADD uv.lock /app/uv.lock
ADD .python-version /app/.python-version

ADD ./alembic.ini /app/alembic.ini
ADD ./alembic /app/alembic

WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD ["/app/.venv/bin/fastapi", "run", "brobot/app.py", "--port", "8000", "--host", "0.0.0.0"]
