from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Suggest using environment variable for prod! Example below:
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Example: replace these details with your Supabase project's credentials
    "postgresql://postgres:[YOUR-PASSWORD]@db.uojnlrqwkzjciogzhask.supabase.co:5432/postgres"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # Helps handle disconnects
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

