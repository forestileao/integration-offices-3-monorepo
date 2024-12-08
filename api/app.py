from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, status, Body, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from watershed import apply_watershed
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import shutil
from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import uuid
from pydantic import PostgresDsn
from datetime import datetime
import os
import asyncio  # For asyncio.gather

SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql",
    user=os.environ.get("POSTGRES_USER") or 'your_username',
    password=os.environ.get("POSTGRES_PASSWORD") or 'your_password',
    host=os.environ.get("POSTGRES_HOST") or 'localhost',
    path=os.environ.get("POSTGRES_DB") or '/your_database',
)

ASYNC_SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql+asyncpg",  # Use asyncpg for async operations
    user=os.environ.get("POSTGRES_USER") or 'your_username',
    password=os.environ.get("POSTGRES_PASSWORD") or 'your_password',
    host=os.environ.get("POSTGRES_HOST") or 'localhost',
    path=os.environ.get("POSTGRES_DB") or '/your_database',
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)


SECRET_KEY = os.environ.get('SECRET_KEY') or "dasuhjfsdaiufdasoduasioudasiudiasuioduasioduasio"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365 * 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Create a passlib context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function to hash a password
def hash_password(password: str):
    return pwd_context.hash(password)

# Function to verify a password against a hashed one
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None



# SQLAlchemy setup
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
assync_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

def initialize_database():
    schema_path = "database.sql"
    if os.path.exists(schema_path):
        connection = engine.raw_connection()  # Get raw SQLite connection
        try:
            with open(schema_path, "r") as schema_file:
                sql_script = schema_file.read()
            cursor = connection.cursor()
            cursor.execute(sql_script)
            connection.commit()
        finally:
            connection.close()  # Ensure the connection is closed
    else:
        print(f"Schema file '{schema_path}' not found.")

# OAuth2PasswordBearer will expect a token in the "Authorization" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    deleted = Column(Integer, default=0)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

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
    waterLevel = Column(Float, nullable=False)
    soilMoisture = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    async with assync_session() as session:
        yield session

def get_current_user(request: Request):

    token = request.headers.get("Authorization")

    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    token = token.split(" ")[1]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

# CRUD Operations
@app.post("/projects/", response_model=dict)
def create_project(body = Body(), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    project = Project(name=body["name"])
    db.add(project)
    db.commit()
    db.refresh(project)

    # create chambers for the project, with default parameters

    chambersCount = body["chambersCount"]

    for i in range(chambersCount):
        chamber = Chamber(name=f"Chamber {i+1}", projectId=project.id)
        db.add(chamber)
        db.commit()
        db.refresh(chamber)

        parameter = Parameter(
            chamberId=chamber.id,
            soilMoistureLowerLimit=60,
            lightingRoutine='07:40/18:20',
            temperatureRange='20',
            ventilationSchedule='10:00/11:00',
            photoCaptureFrequency='60'
        )
        db.add(parameter)
        db.commit()
        db.refresh(parameter)

    # assign admin role to the user in this project

    role = db.query(Role).filter(Role.roleName == "admin").first()
    user = db.query(User).filter(User.id == current_user["sub"]).first()
    role_user = RoleUser(userId=user.id, roleId=role.id, projectId=project.id)

    db.add(role_user)
    db.commit()
    return {"id": project.id, "name": project.name}

@app.get("/projects/", response_model=list)
def list_projects(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Get the user's roles in the project (admin or viewer)
    role_user_data = db.query(Project, RoleUser.roleId, Role.roleName) \
        .join(RoleUser, RoleUser.projectId == Project.id) \
        .join(Role, Role.id == RoleUser.roleId) \
        .filter(RoleUser.userId == current_user["sub"]) \
        .filter(Project.deleted == 0) \
        .all()

    projects = [
        {
            "id": project.id,
            "name": project.name,
            "role": role_name
        }
        for project, role_id, role_name in role_user_data
    ]

    return projects

@app.get("/projects/{project_id}/", response_model=dict)
async def get_project(project_id: str, db: AsyncSession = Depends(get_async_db), current_user: dict = Depends(get_current_user)):
    role_user_data = await db.query(Project, RoleUser.roleId, Role.roleName) \
        .join(RoleUser, RoleUser.projectId == Project.id) \
        .join(Role, Role.id == RoleUser.roleId) \
        .filter(RoleUser.userId == current_user["sub"]) \
        .filter(Project.deleted == 0) \
        .filter(Project.id == project_id) \
        .first()

    if not role_user_data:
        raise HTTPException(status_code=404, detail="Project not found")

    # get parameters, chambers, estimates for the project
    chambers = await db.query(Chamber).filter(Chamber.projectId == project_id).all()
    parameters_task = asyncio.create_task(db.query(Parameter).filter(Parameter.chamberId.in_([c.id for c in chambers])).all())
    estimates_task = asyncio.create_task(db.query(Estimate).filter(Estimate.chamberId.in_([c.id for c in chambers])).all())

    project, _role_id, role_name = role_user_data
    return {
        "id": project.id,
        "name": project.name,
        "role": role_name,
        "chambers": chambers,
        "parameters": [p async for p in (await parameters_task).scalars()],
        "estimates": [e async for e in (await estimates_task).scalars()]
        }

@app.delete("/projects/{project_id}/", response_model=dict)
def delete_project(project_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.deleted = 1
    db.commit()
    return {"message": "Project deleted"}



@app.post("/users/", response_model=dict)
def create_user(username: str = Body(), password: str = Body(), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, password= hash_password(password))

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create the JWT token with the user's ID
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    return {"id": user.id, "username": user.username, "access_token": access_token}

@app.get("/users/", response_model=list)
def list_users(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "projectId": u.projectId} for u in users]

# Example for Chambers
@app.post("/chambers/", response_model=dict)
def create_chamber(name: str, projectId: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    chamber = Chamber(name=name, projectId=projectId)
    db.add(chamber)
    db.commit()
    db.refresh(chamber)
    return {"id": chamber.id, "name": chamber.name}

@app.get("/chambers/", response_model=list)
def list_chambers(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    chambers = db.query(Chamber).all()
    return [{"id": c.id, "name": c.name, "projectId": c.projectId} for c in chambers]

@app.get("/chamber/parameters/{chamber_id}/", response_model=dict)
def get_chamber_parameters(chamber_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    parameters = db.query(Parameter).filter(Parameter.chamberId == chamber_id).first()
    return {
        "id": parameters.id,
        "chamberId": parameters.chamberId,
        "soilMoistureLowerLimit": parameters.soilMoistureLowerLimit,
        "lightingRoutine": parameters.lightingRoutine,
        "temperatureRange": parameters.temperatureRange,
        "ventilationSchedule": parameters.ventilationSchedule,
        "photoCaptureFrequency": parameters.photoCaptureFrequency
    }

# Create Parameters
@app.post("/parameters/", response_model=dict)
def create_parameter(chamberId: str = Body(), soilMoistureLowerLimit: float = Body(), lightingRoutine: str = Body(),
                     temperatureRange: str = Body(), ventilationSchedule: str = Body(), photoCaptureFrequency: str = Body(),
                     db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    current_parameter = db.query(Parameter).filter(Parameter.chamberId == chamberId).first()

    # update current parameter if exists
    if current_parameter:
        current_parameter.soilMoistureLowerLimit = soilMoistureLowerLimit
        current_parameter.lightingRoutine = lightingRoutine
        current_parameter.temperatureRange = temperatureRange
        current_parameter.ventilationSchedule = ventilationSchedule
        current_parameter.photoCaptureFrequency = photoCaptureFrequency
        db.commit()
        return {"id": current_parameter.id, "chamberId": current_parameter.chamberId}

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
def list_parameters(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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


@app.get("/chamber/photo/{chamber_id}/", response_model=dict)
def list_photos(chamber_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    photos = db.query(Photo).filter(Photo.chamberId == chamber_id).all()
    return [{"id": p.id, "chamberId": p.chamberId, "captureDate": p.captureDate, "imageUrl": p.imageUrl} for p in photos]

# get photo from disk and display binary
@app.get("/photo/{photo_id}/")
def get_photo(photo_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    photo = db.query(Photo).filter(Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    with open(photo.imageUrl, "rb") as img_file:
        img_stream = img_file.read()

    return StreamingResponse(content=img_stream, media_type="image/jpeg")


@app.post("/photos/", response_model=dict)
def create_photo(chamberId: str, photo: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    binary = photo.file.read()
    marked_binary, green_area, leaf_count = apply_watershed(binary)

    # Generate a unique filename for the uploaded image
    file_location = f"uploads/{generate_uuid()}_{photo.filename}"

    # Save the file to the local filesystem
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(marked_binary, buffer)

    # update last estimate with the new photo
    last_estimate = db.query(Estimate) \
        .filter(Estimate.chamberId == chamberId) \
        .filter(Estimate.greenArea == 99999) \
        .order_by(Estimate.estimateDate.desc()).first()

    if last_estimate:
        last_estimate.greenArea = green_area
        last_estimate.leafCount = leaf_count
        db.commit()

    # Create a new Photo entry in the database
    photo_entry = Photo(chamberId=chamberId, imageUrl=file_location)
    db.add(photo_entry)
    db.commit()
    db.refresh(photo_entry)

    # Return the photo details
    return {"id": photo_entry.id, "chamberId": photo_entry.chamberId, "imageUrl": photo_entry.imageUrl}

@app.get("/photos/", response_model=list)
def list_photos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    photos = db.query(Photo).all()
    return [{"id": p.id, "chamberId": p.chamberId, "captureDate": p.captureDate, "imageUrl": p.imageUrl} for p in photos]

# Create Estimates
@app.post("/estimates/", response_model=dict)
def create_estimate(chamberId: str = Body(), leafCount: int = Body(), greenArea: float = Body(), estimateDate: datetime = Body(),
                    soilMoisture: float = Body(), temperature: float = Body(), humidity: float = Body(),
                    waterLevel: float = Body(),
                    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    estimate = Estimate(chamberId=chamberId, leafCount=leafCount, greenArea=greenArea, estimateDate=estimateDate or datetime.utcnow(),
                        soilMoisture=soilMoisture, temperature=temperature, humidity=humidity, waterLevel=waterLevel)
    db.add(estimate)
    db.commit()
    db.refresh(estimate)
    return {"id": estimate.id, "chamberId": estimate.chamberId, "leafCount": estimate.leafCount, "greenArea": estimate.greenArea}

# get estimates by optional chamberId
@app.get("/estimates/", response_model=list)
def list_estimates(chamberId = None, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if chamberId:
        estimates = db.query(Estimate).filter(Estimate.chamberId == chamberId).all()
        return [{"id": e.id, "chamberId": e.chamberId, "leafCount": e.leafCount, "greenArea": e.greenArea, "estimateDate": e.estimateDate, "waterLevel": e.waterLevel} for e in estimates]

    estimates = db.query(Estimate).all()
    return [{"id": e.id, "chamberId": e.chamberId, "leafCount": e.leafCount, "greenArea": e.greenArea, "estimateDate": e.estimateDate} for e in estimates]

# Create Permissions
@app.post("/permissions/", response_model=dict)
def create_permission(label: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    permission = Permission(label=label)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return {"id": permission.id, "label": permission.label}

@app.get("/permissions/", response_model=list)
def list_permissions(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    permissions = db.query(Permission).all()
    return [{"id": p.id, "label": p.label} for p in permissions]

# Create Roles
@app.post("/roles/", response_model=dict)
def create_role(roleName: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    role = Role(roleName=roleName)
    db.add(role)
    db.commit()
    db.refresh(role)
    return {"id": role.id, "roleName": role.roleName}

@app.get("/roles/", response_model=list)
def list_roles(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    roles = db.query(Role).all()
    return [{"id": r.id, "roleName": r.roleName} for r in roles]

# Create User Permissions
@app.post("/user_permissions/", response_model=dict)
def create_user_permission(permissionId: str, roleId: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_permission = UserPermission(permissionId=permissionId, roleId=roleId)
    db.add(user_permission)
    db.commit()
    db.refresh(user_permission)
    return {"id": user_permission.id, "permissionId": user_permission.permissionId, "roleId": user_permission.roleId}

@app.get("/user_permissions/", response_model=list)
def list_user_permissions(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_permissions = db.query(UserPermission).all()
    return [{"id": up.id, "permissionId": up.permissionId, "roleId": up.roleId} for up in user_permissions]

# Create Role User
@app.post("/role_user/", response_model=dict)
def create_role_user(username: str = Body(), roleId: str = Body(), projectId: str = Body(), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.username == username).first()
    role_user = RoleUser(userId=user.id, roleId=roleId, projectId=projectId)
    db.add(role_user)
    db.commit()
    db.refresh(role_user)
    return {"id": role_user.id, "userId": role_user.userId, "roleId": role_user.roleId, "projectId": role_user.projectId}

@app.get("/role_user/", response_model=list)
def list_role_users(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    role_users = db.query(RoleUser).all()
    return [{"id": ru.id, "userId": ru.userId, "roleId": ru.roleId, "projectId": ru.projectId} for ru in role_users]


@app.post("/token", response_model=dict)
async def login_for_access_token(username = Body(), password = Body(), db: Session = Depends(get_db)):
    # Fetch the user from the database
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create the JWT token with the user's ID
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
