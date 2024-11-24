from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import shutil
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
    projectId = Column(String, ForeignKey("projects.id"))

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

# Create Parameters
@app.post("/parameters/", response_model=dict)
def create_parameter(chamberId: str, soilMoistureLowerLimit: float, lightingRoutine: str,
                     temperatureRange: str, ventilationSchedule: str, photoCaptureFrequency: str,
                     db: Session = Depends(get_db)):
    parameter = Parameter(
        chamberId=chamberId,
        soilMoistureLowerLimit=soilMoistureLowerLimit,
        lightingRoutine=lightingRoutine,
        temperatureRange=temperatureRange,
        ventilationSchedule=ventilationSchedule,
        photoCaptureFrequency=photoCaptureFrequency
    )
    db.add(parameter)
    db.commit()
    db.refresh(parameter)
    return {"id": parameter.id, "chamberId": parameter.chamberId}

@app.get("/parameters/", response_model=list)
def list_parameters(db: Session = Depends(get_db)):
    parameters = db.query(Parameter).all()
    return [{
        "id": p.id,
        "chamberId": p.chamberId,
        "soilMoistureLowerLimit": p.soilMoistureLowerLimit,
        "lightingRoutine": p.lightingRoutine,
        "temperatureRange": p.temperatureRange,
        "ventilationSchedule": p.ventilationSchedule,
        "photoCaptureFrequency": p.photoCaptureFrequency
    } for p in parameters]

@app.post("/photos/", response_model=dict)
def create_photo(chamberId: str, photo: UploadFile = File(...), db: Session = Depends(get_db)):
    # Generate a unique filename for the uploaded image
    file_location = f"uploads/{generate_uuid()}_{photo.filename}"

    # Save the file to the local filesystem
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # Create a new Photo entry in the database
    photo_entry = Photo(chamberId=chamberId, imageUrl=file_location)
    db.add(photo_entry)
    db.commit()
    db.refresh(photo_entry)

    # Return the photo details
    return {"id": photo_entry.id, "chamberId": photo_entry.chamberId, "imageUrl": photo_entry.imageUrl}

@app.get("/photos/", response_model=list)
def list_photos(db: Session = Depends(get_db)):
    photos = db.query(Photo).all()
    return [{"id": p.id, "chamberId": p.chamberId, "captureDate": p.captureDate, "imageUrl": p.imageUrl} for p in photos]

# Create Estimates
@app.post("/estimates/", response_model=dict)
def create_estimate(chamberId: str, leafCount: int, greenArea: float, estimateDate: datetime = None,
                    db: Session = Depends(get_db)):
    estimate = Estimate(chamberId=chamberId, leafCount=leafCount, greenArea=greenArea, estimateDate=estimateDate or datetime.utcnow())
    db.add(estimate)
    db.commit()
    db.refresh(estimate)
    return {"id": estimate.id, "chamberId": estimate.chamberId, "leafCount": estimate.leafCount, "greenArea": estimate.greenArea}

@app.get("/estimates/", response_model=list)
def list_estimates(db: Session = Depends(get_db)):
    estimates = db.query(Estimate).all()
    return [{"id": e.id, "chamberId": e.chamberId, "leafCount": e.leafCount, "greenArea": e.greenArea, "estimateDate": e.estimateDate} for e in estimates]

# Create Permissions
@app.post("/permissions/", response_model=dict)
def create_permission(label: str, db: Session = Depends(get_db)):
    permission = Permission(label=label)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return {"id": permission.id, "label": permission.label}

@app.get("/permissions/", response_model=list)
def list_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return [{"id": p.id, "label": p.label} for p in permissions]

# Create Roles
@app.post("/roles/", response_model=dict)
def create_role(roleName: str, db: Session = Depends(get_db)):
    role = Role(roleName=roleName)
    db.add(role)
    db.commit()
    db.refresh(role)
    return {"id": role.id, "roleName": role.roleName}

@app.get("/roles/", response_model=list)
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return [{"id": r.id, "roleName": r.roleName} for r in roles]

# Create User Permissions
@app.post("/user_permissions/", response_model=dict)
def create_user_permission(permissionId: str, roleId: str, db: Session = Depends(get_db)):
    user_permission = UserPermission(permissionId=permissionId, roleId=roleId)
    db.add(user_permission)
    db.commit()
    db.refresh(user_permission)
    return {"id": user_permission.id, "permissionId": user_permission.permissionId, "roleId": user_permission.roleId}

@app.get("/user_permissions/", response_model=list)
def list_user_permissions(db: Session = Depends(get_db)):
    user_permissions = db.query(UserPermission).all()
    return [{"id": up.id, "permissionId": up.permissionId, "roleId": up.roleId} for up in user_permissions]

# Create Role User
@app.post("/role_user/", response_model=dict)
def create_role_user(userId: str, roleId: str, projectId: str, db: Session = Depends(get_db)):
    role_user = RoleUser(userId=userId, roleId=roleId, projectId=projectId)
    db.add(role_user)
    db.commit()
    db.refresh(role_user)
    return {"id": role_user.id, "userId": role_user.userId, "roleId": role_user.roleId, "projectId": role_user.projectId}

@app.get("/role_user/", response_model=list)
def list_role_users(db: Session = Depends(get_db)):
    role_users = db.query(RoleUser).all()
    return [{"id": ru.id, "userId": ru.userId, "roleId": ru.roleId, "projectId": ru.projectId} for ru in role_users]


@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Fetch the user from the database
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create the JWT token with the user's ID
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
