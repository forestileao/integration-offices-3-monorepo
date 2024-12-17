# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc && \
    rm -rf /var/lib/apt/lists/*


# Copy the application code into the container
COPY . .

# Ensure that the schema.sql file is present inside the container
RUN if [ -f database.sql ]; then echo "Schema file found."; else echo "Schema file not found."; fi

VOLUME /app/uploads

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the application using Uvicorn
CMD ["sh", "-c", "mkdir -p /app/uploads && uvicorn app:app --host 0.0.0.0 --port 8000 --reload"]
