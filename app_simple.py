from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# In-memory storage for demo purposes
athletes = []
events = []
competitions = []

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', 
                         athletes_count=len(athletes),
                         events_count=len(events),
                         competitions_count=len(competitions))

@app.route('/athletes')
def athletes_page():
    """Athletes page"""
    return render_template('athletes.html', athletes=athletes)

@app.route('/events')
def events_page():
    """Events page"""
    return render_template('events.html', events=events)

@app.route('/competitions')
def competitions_page():
    """Competitions page"""
    return render_template('competitions.html', competitions=competitions)

@app.route('/api/athletes', methods=['GET', 'POST'])
def api_athletes():
    """API endpoint for athletes"""
    if request.method == 'POST':
        data = request.get_json()
        athlete = {
            'id': len(athletes) + 1,
            'name': data['name'],
            'age': data['age'],
            'sport': data['sport'],
            'personal_best': data.get('personal_best', ''),
            'achievements': data.get('achievements', ''),
            'created_at': datetime.utcnow()
        }
        athletes.append(athlete)
        return jsonify({'message': 'Athlete created successfully', 'id': athlete['id']}), 201
    
    return jsonify(athletes)

@app.route('/api/events', methods=['GET', 'POST'])
def api_events():
    """API endpoint for events"""
    if request.method == 'POST':
        data = request.get_json()
        event = {
            'id': len(events) + 1,
            'name': data['name'],
            'event_type': data['event_type'],
            'description': data.get('description', ''),
            'date': datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else None,
            'created_at': datetime.utcnow()
        }
        events.append(event)
        return jsonify({'message': 'Event created successfully', 'id': event['id']}), 201
    
    return jsonify(events)

@app.route('/api/competitions', methods=['GET', 'POST'])
def api_competitions():
    """API endpoint for competitions"""
    if request.method == 'POST':
        data = request.get_json()
        competition = {
            'id': len(competitions) + 1,
            'name': data['name'],
            'location': data['location'],
            'start_date': datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            'end_date': datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            'description': data.get('description', ''),
            'created_at': datetime.utcnow()
        }
        competitions.append(competition)
        return jsonify({'message': 'Competition created successfully', 'id': competition['id']}), 201
    
    return jsonify(competitions)

if __name__ == '__main__':
    print("Starting Grenada Athletics application...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)




