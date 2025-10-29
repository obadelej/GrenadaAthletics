@echo off
echo Installing Grenada Athletics Dependencies...
echo.

echo Installing Flask...
python -m pip install Flask --user
if %errorlevel% neq 0 (
    echo Failed to install Flask
    pause
    exit /b 1
)

echo Installing Flask-SQLAlchemy...
python -m pip install Flask-SQLAlchemy --user
if %errorlevel% neq 0 (
    echo Failed to install Flask-SQLAlchemy
    pause
    exit /b 1
)

echo Installing Flask-Migrate...
python -m pip install Flask-Migrate --user
if %errorlevel% neq 0 (
    echo Failed to install Flask-Migrate
    pause
    exit /b 1
)

echo Installing psycopg2-binary...
python -m pip install psycopg2-binary --user
if %errorlevel% neq 0 (
    echo Failed to install psycopg2-binary
    pause
    exit /b 1
)

echo Installing python-dotenv...
python -m pip install python-dotenv --user
if %errorlevel% neq 0 (
    echo Failed to install python-dotenv
    pause
    exit /b 1
)

echo Installing Werkzeug...
python -m pip install Werkzeug --user
if %errorlevel% neq 0 (
    echo Failed to install Werkzeug
    pause
    exit /b 1
)

echo.
echo All dependencies installed successfully!
echo You can now run the application with: python app.py
pause




