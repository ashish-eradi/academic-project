# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import students, auth, attendance, grades, timetables, parents, staff, finance, communication, analytics, users
from app.database import engine, Base
from app import models

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Academic - School Management System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")
app.include_router(attendance.router, prefix="/api/v1")
app.include_router(grades.router, prefix="/api/v1")
app.include_router(timetables.router, prefix="/api/v1")
app.include_router(parents.router, prefix="/api/v1")
app.include_router(staff.router, prefix="/api/v1")
app.include_router(finance.router, prefix="/api/v1")
app.include_router(communication.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Project Academic - School Management System"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}