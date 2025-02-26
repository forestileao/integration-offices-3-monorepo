# Plant Monitoring System

This project is a Plant Monitoring System built with FastAPI for the backend and Next.js for the frontend.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Learn More](#learn-more)

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Setup

### Backend

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>/api
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Initialize the database:

   ```sh
   python -c "from app import initialize_database; initialize_database()"
   ```

### Frontend

1. Navigate to the `webapp` directory:

   ```sh
   cd ../webapp
   ```

2. Install the dependencies:

   ```sh
   npm install
   # or
   yarn install
   ```

## Running the Project

### Backend

1. Start the FastAPI server:

   ```sh
   uvicorn app:app --reload
   ```

   The backend server will be running at [http://localhost:8000](http://localhost:8000).

### Frontend

1. Start the Next.js development server:

   ```sh
   npm run dev
   # or
   yarn dev
   ```

   The frontend server will be running at [http://localhost:3000](http://localhost:3000).

## Project Structure

### Backend

- `api/app.py`: Main FastAPI application file containing models, routes, and utility functions.
- `api/database.sql`: SQL script to initialize the database schema.

### Frontend

- `webapp/app/add-user/page.tsx`: Page for adding a new user.
- `webapp/app/create-account/page.tsx`: Page for creating a new account.
- `webapp/components/ui`: UI components used in the frontend.
- `webapp/hooks`: Custom hooks used in the frontend.
- `webapp/api`: API functions to interact with the backend.

## API Endpoints

- `POST /projects/`: Create a new project.
- `GET /projects/`: List all projects.
- `POST /token`: Obtain a JWT token.
- `POST /users/`: Create a new user.

## Learn More

To learn more about the technologies used in this project, take a look at the following resources:

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
