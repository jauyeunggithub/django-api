@echo off

REM Ensure that Docker Compose is running and rebuild containers
echo Starting Docker Compose and rebuilding containers...
docker-compose up --build -d

REM Remove the existing SQLite database file (if it exists)
echo Removing existing SQLite database file...
docker-compose exec app rm -f /app/db.sqlite3

REM Install dependencies inside the container
echo Installing dependencies...
docker-compose exec app pip install -r /app/requirements.txt

REM Automatically run Django database migrations
echo Running migrations...
docker-compose exec app python /app/manage.py migrate

REM Run the unit tests
echo Running tests...
docker-compose exec app python /app/manage.py test

REM Optionally, stop the containers after tests are done
echo Stopping Docker Compose containers...
docker-compose down
