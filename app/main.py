# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/health")
# def health():
#     return {"status": "ok"}

from fastapi import FastAPI
from app.db.database import engine

app = FastAPI()


@app.get("/health/db")
def check_db():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"db": "connected"}
    except Exception as e:
        return {"db": "error", "detail": str(e)}
