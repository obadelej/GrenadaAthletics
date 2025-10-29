# Grenada Athletics - Setup Guide

## Current Status
✅ **Python 3.13.7** - Installed and working  
✅ **PostgreSQL 18.0** - Installed and available  
✅ **Virtual environment** - Created at `.venv`  
✅ **Python packages** - Installed in `.venv`  

## Project Structure Created
```
GrenadaAthletics/
├── app.py                 # Main Flask application (with PostgreSQL)
├── app_simple.py          # Simplified version (no database required)
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── install_dependencies.bat  # Windows batch script for installation
├── .env                   # Environment variables
├── README.md             # Project documentation
├── SETUP_GUIDE.md        # This setup guide
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── athletes.html
│   ├── events.html
│   └── competitions.html
└── static/               # Static assets
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Installation Options

### Option 1: Quick Start with Virtual Environment (Recommended)
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### Option 2: Manual Installation in venv
Install packages one by one inside the activated venv:
```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate psycopg[binary] python-dotenv Werkzeug
```

### Option 3: Using Conda (if available)
```bash
conda install flask flask-sqlalchemy psycopg2 python-dotenv
```

## Running the Application

### Option A: Simple Version (No Database)
```bash
python app_simple.py
```
- Uses in-memory storage
- No database setup required
- Perfect for testing and development

### Option B: Full Version (With PostgreSQL)
1. **Create PostgreSQL database:**
   ```bash
   psql -U postgres
   CREATE DATABASE grenada_athletics;
   \q
   ```

2. **Update .env file:**
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://postgres:your_password@localhost/grenada_athletics
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## Accessing the Application
Once running, open your browser and go to:
- **Main page:** http://localhost:5000
- **Athletes:** http://localhost:5000/athletes
- **Events:** http://localhost:5000/events
- **Competitions:** http://localhost:5000/competitions

## Features Available
- ✅ Modern responsive UI with red, black, and gold color scheme
- ✅ Athlete management (add, view athletes)
- ✅ Event management (add, view events)
- ✅ Competition management (add, view competitions)
- ✅ RESTful API endpoints
- ✅ Real-time data updates
- ✅ Mobile-friendly design

## Troubleshooting

### If pip installation fails:
1. Ensure the virtual environment is active
2. Upgrade pip: `python -m pip install --upgrade pip`
3. Use psycopg v3 wheels instead of psycopg2: `pip install psycopg[binary]`

### If PostgreSQL connection fails:
1. Make sure PostgreSQL service is running
2. Check the connection string in .env file
3. Verify username and password are correct

### If the application won't start:
1. Check if all dependencies are installed: `python -c "import flask"`
2. Check for any error messages in the console
3. Try the simple version first: `python app_simple.py`

## Next Steps
1. Install dependencies using one of the methods above
2. Start with the simple version to test functionality
3. Set up PostgreSQL for the full version
4. Customize the application for your specific needs

## Support
If you encounter any issues, check the error messages and try the troubleshooting steps above.

