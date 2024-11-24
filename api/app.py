from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import uuid
from datetime import datetime
import os

DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():
    schema_path = "database.sql"
    if os.path.exists(schema_path):
        connection = engine.raw_connection()  # Get raw SQLite connection
        try:
            with open(schema_path, "r") as schema_file:
                sql_script = schema_file.read()
            cursor = connection.cursor()
            cursor.executescript(sql_script)  # Execute SQL script
            connection.commit()
        finally:
            connection.close()  # Ensure the connection is closed
    else:
        print(f"Schema file '{schema_path}' not found.")



# Run the schema.sql at the start
initialize_database()

# Helper function to generate UUID
def generate_uuid():
    return str(uuid.uuid4())

# Models
class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    projectId = Column(String, ForeignKey("projects.id"))

class Chamber(Base):
    __tablename__ = "chambers"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    projectId = Column(String, ForeignKey("projects.id"))

class Parameter(Base):
    __tablename__ = "parameters"
    id = Column(String, primary_key=True, default=generate_uuid)
    chamberId = Column(String, ForeignKey("chambers.id"))
    soilMoistureLowerLimit = Column(Float, nullable=False)
    lightingRoutine = Column(String, nullable=False)
    temperatureRange = Column(String, nullable=False)
    ventilationSchedule = Column(String, nullable=False)
    photoCaptureFrequency = Column(String, nullable=False)

class Photo(Base):
    __tablename__ = "photos"
    id = Column(String, primary_key=True, default=generate_uuid)
    chamberId = Column(String, ForeignKey("chambers.id"))
    captureDate = Column(DateTime, default=datetime.utcnow)
    imageUrl = Column(String, nullable=False)

class Estimate(Base):
    __tablename__ = "estimates"
    id = Column(String, primary_key=True, default=generate_uuid)
    chamberId = Column(String, ForeignKey("chambers.id"))
    leafCount = Column(Integer, nullable=False)
    greenArea = Column(Float, nullable=False)
    estimateDate = Column(DateTime, default=datetime.utcnow)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True, default=generate_uuid)
    label = Column(String, nullable=False)

class Role(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True, default=generate_uuid)
    roleName = Column(String, nullable=False)

class UserPermission(Base):
    __tablename__ = "user_permissions"
    id = Column(String, primary_key=True, default=generate_uuid)
    permissionId = Column(String, ForeignKey("permissions.id"))
    roleId = Column(String, ForeignKey("roles.id"))

class RoleUser(Base):
    __tablename__ = "role_user"
    id = Column(String, primary_key=True, default=generate_uuid)
    userId = Column(String, ForeignKey("users.id"))
    roleId = Column(String, ForeignKey("roles.id"))

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations
@app.post("/projects/", response_model=dict)
def create_project(name: str, db: Session = Depends(get_db)):
    project = Project(name=name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name}

@app.get("/projects/", response_model=list)
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{"id": p.id, "name": p.name} for p in projects]

@app.post("/users/", response_model=dict)
def create_user(username: str, password: str, projectId: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, password=password, projectId=projectId)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

@app.get("/users/", response_model=list)
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "projectId": u.projectId} for u in users]

# Example for Chambers
@app.post("/chambers/", response_model=dict)
def create_chamber(name: str, projectId: str, db: Session = Depends(get_db)):
    chamber = Chamber(name=name, projectId=projectId)
    db.add(chamber)
    db.commit()
    db.refresh(chamber)
    return {"id": chamber.id, "name": chamber.name}

@app.get("/chambers/", response_model=list)
def list_chambers(db: Session = Depends(get_db)):
    chambers = db.query(Chamber).all()
    return [{"id": c.id, "name": c.name, "projectId": c.projectId} for c in chambers]

# Additional routes for Parameters, Photos, Estimates, Roles, etc., can follow the same pattern.
