FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install --no-cache-dir streamlit requests

COPY frontend/ ./frontend/

EXPOSE 8501

CMD ["sh", "-c", "streamlit run frontend/streamlit_app.py --server.address=0.0.0.0 --server.port=${PORT:-8501} --server.headless=true"]