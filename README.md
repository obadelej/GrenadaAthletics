# Grenada Athletics

A modern web application for managing athletes, events, and competitions in Grenada.

## Features

- **Athlete Management**: Track athlete profiles, personal bests, and achievements
- **Event Planning**: Organize and manage athletic events
- **Competition Tracking**: Monitor competitions and their status
- **Modern UI**: Responsive design with red, black, and gold color scheme
- **RESTful API**: JSON API endpoints for data management

## Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome

## Prerequisites

- Python 3.7+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GrenadaAthletics
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb grenada_athletics
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE grenada_athletics;
   \q
   ```

5. **Configure environment variables**
   - Copy `.env` file and update the database URL with your PostgreSQL credentials
   - Update the `SECRET_KEY` for production use

6. **Initialize the database**
   ```bash
   python app.py
   # The database tables will be created automatically on first run
   ```

## Running the Application

1. **Start the Flask development server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

## API Endpoints

### Athletes
- `GET /api/athletes` - Get all athletes
- `POST /api/athletes` - Create a new athlete

### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create a new event

### Competitions
- `GET /api/competitions` - Get all competitions
- `POST /api/competitions` - Create a new competition

## Project Structure

```
GrenadaAthletics/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # Project documentation
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

## Development

### Adding New Features
1. Create new routes in `app.py`
2. Add corresponding database models in `models.py`
3. Create HTML templates in `templates/`
4. Add JavaScript functionality in `static/js/main.js`
5. Update CSS styles in `static/css/style.css`

### Database Migrations
The application uses Flask-Migrate for database schema management:
```bash
# Initialize migrations (first time only)
flask db init

# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

## Production Deployment

1. **Set production environment variables**
   - Update `SECRET_KEY` to a secure random string
   - Configure proper `DATABASE_URL` for production database
   - Set `FLASK_ENV=production`

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Configure reverse proxy** (nginx recommended)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team.

## Version Control

Initialize and connect to GitHub:

```bash
# From project root
git init
git branch -M main
# Add a remote after you create a GitHub repository
# git remote add origin https://github.com/<your-username>/<your-repo>.git
# First commit
git add .
git commit -m "Initial commit: modular Flask app setup"
# Push
# git push -u origin main
```

