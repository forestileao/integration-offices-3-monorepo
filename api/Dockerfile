# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Ensure that the schema.sql file is present inside the container
RUN if [ -f database.sql ]; then echo "Schema file found."; else echo "Schema file not found."; fi

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
