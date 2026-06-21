import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Build an absolute path to the database to prevent Streamlit CWD issues
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_db_path = os.path.join(BASE_DIR, "economic_data.db")
default_db_url = f"sqlite:///{default_db_path}"

# Default to SQLite if DATABASE_URL is not set
DATABASE_URL = os.getenv("DATABASE_URL", default_db_url)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
