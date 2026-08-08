FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "uv run uvicorn app:app --host 127.0.0.1 --port 8000 & exec uv run streamlit frontend/streamlit_app.py --server.address=0.0.0.0 --server.port=${PORT:-10000} --server.headless=true"]