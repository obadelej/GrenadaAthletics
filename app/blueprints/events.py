from flask import Blueprint, render_template, request, jsonify, flash
from app.models import Event
from extensions import db
from datetime import datetime

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
def events():
    """Events page"""
    events = Event.query.all()
    return render_template('events.html', events=events)

@events_bp.route('/api', methods=['GET', 'POST'])
def api_events():
    """API endpoint for events"""
    if request.method == 'POST':
        data = request.get_json()
        event = Event(
            name=data['name'],
            event_type=data['event_type'],
            description=data.get('description', ''),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else None
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully', 'id': event.id}), 201
    
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])
