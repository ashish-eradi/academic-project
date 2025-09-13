# app/init_db.py
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.database import Base
# Import ALL models to ensure they are registered with the Base
# This is crucial for Base.metadata.create_all() to work
from app.models import user, student, attendance, grade, timetable, parent, staff, finance, communication, analytics

# Use SQLite for simplicity (adjust for production DB)
SQLALCHEMY_DATABASE_URL = "sqlite:///./academic.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    # Create all tables defined in models and imported above
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
