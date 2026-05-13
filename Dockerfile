FROM python:3.12

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic downgrade base && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]