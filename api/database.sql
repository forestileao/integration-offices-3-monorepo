  -- Create Projects table
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    deleted int DEFAULT 0
);

-- Create Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Create Chambers table
CREATE TABLE IF NOT EXISTS chambers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    "projectId" TEXT,
    FOREIGN KEY ("projectId") REFERENCES projects (id)
);

-- Create Parameters table
CREATE TABLE IF NOT EXISTS parameters (
    id TEXT PRIMARY KEY,
    "chamberId" TEXT NOT NULL,
    "soilMoistureLowerLimit" REAL NOT NULL,
    "lightingRoutine" TEXT NOT NULL,
    "temperatureRange" TEXT NOT NULL,
    "ventilationSchedule" TEXT NOT NULL,
    "photoCaptureFrequency" TEXT NOT NULL,
    FOREIGN KEY ("chamberId") REFERENCES chambers (id)
);

-- Create Photos table
CREATE TABLE IF NOT EXISTS photos (
    id TEXT PRIMARY KEY,
    "chamberId" TEXT NOT NULL,
    "captureDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "imageUrl" TEXT NOT NULL,
    FOREIGN KEY ("chamberId") REFERENCES chambers (id)
);

-- Create Estimates table
CREATE TABLE IF NOT EXISTS estimates (
    id TEXT PRIMARY KEY,
    "chamberId" TEXT NOT NULL,
    "leafCount" INTEGER NOT NULL,
    "greenArea" REAL NOT NULL,
    "soilMoisture" REAL NOT NULL,
    "temperature" REAL NOT NULL,
    "humidity" REAL NOT NULL,
    "estimateDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("chamberId") REFERENCES chambers (id)
);

-- Create Permissions table
CREATE TABLE IF NOT EXISTS permissions (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL
);

-- Create Roles table
CREATE TABLE IF NOT EXISTS roles (
    id TEXT PRIMARY KEY,
    "roleName" TEXT NOT NULL
);

-- Create User Permissions table
CREATE TABLE IF NOT EXISTS user_permissions (
    id TEXT PRIMARY KEY,
    "permissionId" TEXT NOT NULL,
    "roleId" TEXT NOT NULL,
    FOREIGN KEY ("permissionId") REFERENCES permissions (id),
    FOREIGN KEY ("roleId") REFERENCES roles (id)
);

-- Create Role User table
CREATE TABLE IF NOT EXISTS role_user (
    id TEXT PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "roleId" TEXT NOT NULL,
    "projectId" TEXT NOT NULL,
    FOREIGN KEY ("userId") REFERENCES users (id),
    FOREIGN KEY ("roleId") REFERENCES roles (id),
    FOREIGN KEY ("projectId") REFERENCES projects (id)
);


-- Insert 'viewer' role if it doesn't exist
INSERT INTO roles (id, "roleName")
SELECT 'a5f17a1d-d6c7-4e4f-88d5-81b5591f850b', 'viewer'
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE "roleName" = 'viewer');

-- Insert 'admin' role if it doesn't exist
INSERT INTO roles (id, "roleName")
SELECT '1e1a0e30-bfae-4b9c-bb5b-2e9a91f9058d', 'admin'
WHERE NOT EXISTS (SELECT 1 FROM roles WHERE "roleName" = 'admin');



-- Insert permissions for viewing and managing the data, using hardcoded UUIDs
INSERT INTO permissions (id, label)
SELECT '6fe9c6d2-cfe1-44b3-9b2a-b4c9b7223c1d', 'view_projects'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'view_projects');

INSERT INTO permissions (id, label)
SELECT '7a4f2101-1eb5-4877-b967-d2f7b520bdc1', 'view_chambers'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'view_chambers');

INSERT INTO permissions (id, label)
SELECT 'a96e51c4-b574-40de-8dcb-e4c39d9fae33', 'view_parameters'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'view_parameters');

INSERT INTO permissions (id, label)
SELECT '7f3f5177-eec0-47ab-b16a-37aef0b509a0', 'view_photos'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'view_photos');

INSERT INTO permissions (id, label)
SELECT 'f3073d27-2542-4f90-98b7-e05074538ff5', 'view_estimates'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'view_estimates');

INSERT INTO permissions (id, label)
SELECT '5705f902-3f27-41c9-b1fc-d12a70fa1c9e', 'manage_projects'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'manage_projects');

INSERT INTO permissions (id, label)
SELECT '4c2fe70d-1906-46c5-8217-0f9ed4e3c8f5', 'manage_chambers'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'manage_chambers');

INSERT INTO permissions (id, label)
SELECT '9897b7c5-5ee9-4e5a-8ea4-d36e9b0e2b38', 'manage_parameters'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'manage_parameters');

INSERT INTO permissions (id, label)
SELECT 'a62cd59e-e6e5-4bcf-8300-c2faabf9fd8d', 'manage_photos'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'manage_photos');

INSERT INTO permissions (id, label)
SELECT '53a681c5-3b1f-4205-8e26-21f217cfb3b9', 'manage_estimates'
WHERE NOT EXISTS (SELECT 1 FROM permissions WHERE label = 'manage_estimates');


-- Assign permissions to the viewer role (viewer role UUID: 'a5f17a1d-d6c7-4e4f-88d5-81b5591f850b')
INSERT INTO user_permissions (id, "permissionId", "roleId")
SELECT 'e9f6dbdb-393a-4a96-a801-5cdd6b6eaf0a', '6fe9c6d2-cfe1-44b3-9b2a-b4c9b7223c1d', 'a5f17a1d-d6c7-4e4f-88d5-81b5591f850b'
WHERE NOT EXISTS (SELECT 1 FROM user_permissions WHERE "roleId" = 'a5f17a1d-d6c7-4e4f-88d5-81b5591f850b' AND "permissionId" = '6fe9c6d2-cfe1-44b3-9b2a-b4c9b7223c1d');

INSERT INTO user_permissions (id, "permissionId", "roleId")
SELECT 'fa56c5b5-61a4-4b12-84d4-8b907de8e2d1', '7a4f2101-1eb5-4877-b967-d2f7b520bdc1', 'a5f17a1d-d6c7-4e4f-88d5-81b5591f850b'
WHERE NOT EXISTS (SELECT 1 FROM user_permissions WHERE "roleId" = 'a5f17a1d-d6c7-4e4f-88d5-81b5591f850b' AND "permissionId" = '7a4f2101-1eb5-4877-b967-d2f7b520bdc1');

INSERT INTO user_permissions (id, "permissionId", "roleId")
SELECT 'b94db756-4e92-4625-b877-1e263e4b52c0', '5705f902-3f27-41c9-b1fc-d12a70fa1c9e', '1e1a0e30-bfae-4b9c-bb5b-2e9a91f9058d'
WHERE NOT EXISTS (SELECT 1 FROM user_permissions WHERE "roleId" = '1e1a0e30-bfae-4b9c-bb5b-2e9a91f9058d' AND "permissionId" = '5705f902-3f27-41c9-b1fc-d12a70fa1c9e');


alter table estimates add column "waterLevel" real NOT NULL default 0;
