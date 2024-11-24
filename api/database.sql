  -- Create Projects table
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    projectId TEXT,
    FOREIGN KEY (projectId) REFERENCES projects (id)
);

-- Create Chambers table
CREATE TABLE IF NOT EXISTS chambers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    projectId TEXT,
    FOREIGN KEY (projectId) REFERENCES projects (id)
);

-- Create Parameters table
CREATE TABLE IF NOT EXISTS parameters (
    id TEXT PRIMARY KEY,
    chamberId TEXT NOT NULL,
    soilMoistureLowerLimit REAL NOT NULL,
    lightingRoutine TEXT NOT NULL,
    temperatureRange TEXT NOT NULL,
    ventilationSchedule TEXT NOT NULL,
    photoCaptureFrequency TEXT NOT NULL,
    FOREIGN KEY (chamberId) REFERENCES chambers (id)
);

-- Create Photos table
CREATE TABLE IF NOT EXISTS photos (
    id TEXT PRIMARY KEY,
    chamberId TEXT NOT NULL,
    captureDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    imageUrl TEXT NOT NULL,
    FOREIGN KEY (chamberId) REFERENCES chambers (id)
);

-- Create Estimates table
CREATE TABLE IF NOT EXISTS estimates (
    id TEXT PRIMARY KEY,
    chamberId TEXT NOT NULL,
    leafCount INTEGER NOT NULL,
    greenArea REAL NOT NULL,
    estimateDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chamberId) REFERENCES chambers (id)
);

-- Create Permissions table
CREATE TABLE IF NOT EXISTS permissions (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL
);

-- Create Roles table
CREATE TABLE IF NOT EXISTS roles (
    id TEXT PRIMARY KEY,
    roleName TEXT NOT NULL
);

-- Create User Permissions table
CREATE TABLE IF NOT EXISTS user_permissions (
    id TEXT PRIMARY KEY,
    permissionId TEXT NOT NULL,
    roleId TEXT NOT NULL,
    FOREIGN KEY (permissionId) REFERENCES permissions (id),
    FOREIGN KEY (roleId) REFERENCES roles (id)
);

-- Create Role User table
CREATE TABLE IF NOT EXISTS role_user (
    id TEXT PRIMARY KEY,
    userId TEXT NOT NULL,
    roleId TEXT NOT NULL,
    projectId TEXT NOT NULL,
    FOREIGN KEY (userId) REFERENCES users (id),
    FOREIGN KEY (roleId) REFERENCES roles (id),
    FOREIGN KEY (projectId) REFERENCES projects (id)
);
