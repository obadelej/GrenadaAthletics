from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from extensions import db, migrate
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Prefer psycopg v3 driver; auto-upgrade legacy URLs
db_url = os.environ.get('DATABASE_URL', 'postgresql+psycopg://postgres:password@localhost/grenada_athletics')
if db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

# Import models after db initialization
from models import Athlete, Event, Competition

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/athletes')
def athletes():
    """Athletes page"""
    athletes = Athlete.query.all()
    return render_template('athletes.html', athletes=athletes)

@app.route('/events')
def events():
    """Events page"""
    events = Event.query.all()
    return render_template('events.html', events=events)

@app.route('/competitions')
def competitions():
    """Competitions page"""
    competitions = Competition.query.all()
    return render_template('competitions.html', competitions=competitions)

@app.route('/api/athletes', methods=['GET', 'POST'])
def api_athletes():
    """API endpoint for athletes"""
    if request.method == 'POST':
        data = request.get_json()
        athlete = Athlete(
            name=data['name'],
            age=data['age'],
            sport=data['sport'],
            personal_best=data.get('personal_best'),
            achievements=data.get('achievements', '')
        )
        db.session.add(athlete)
        db.session.commit()
        return jsonify({'message': 'Athlete created successfully', 'id': athlete.id}), 201
    
    athletes = Athlete.query.all()
    return jsonify([{
        'id': athlete.id,
        'name': athlete.name,
        'age': athlete.age,
        'sport': athlete.sport,
        'personal_best': athlete.personal_best,
        'achievements': athlete.achievements,
        'created_at': athlete.created_at.isoformat()
    } for athlete in athletes])

@app.route('/api/events', methods=['GET', 'POST'])
def api_events():
    """API endpoint for events"""
    if request.method == 'POST':
        data = request.get_json()
        event = Event(
            name=data['name'],
            event_type=data['event_type'],
            description=data.get('description', ''),
            date=data['date']
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully', 'id': event.id}), 201
    
    events = Event.query.all()
    return jsonify([{
        'id': event.id,
        'name': event.name,
        'event_type': event.event_type,
        'description': event.description,
        'date': event.date.isoformat() if event.date else None,
        'created_at': event.created_at.isoformat()
    } for event in events])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

