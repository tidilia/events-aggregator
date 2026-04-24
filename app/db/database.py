import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_STRING")

engine = create_engine(DATABASE_URL)
