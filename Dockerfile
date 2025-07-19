# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (required for packages like psycopg2 or others with C extensions)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version to avoid any issues with older versions
RUN pip install --upgrade pip

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app will run on (Django default is 8000)
EXPOSE 8000

# Run the Django development server (default port 8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
