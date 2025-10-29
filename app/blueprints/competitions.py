from flask import Blueprint, render_template, request, jsonify, flash
from app.models import Competition
from extensions import db
from datetime import datetime

competitions_bp = Blueprint('competitions', __name__)

@competitions_bp.route('/')
def competitions():
    """Competitions page"""
    competitions = Competition.query.all()
    return render_template('competitions.html', competitions=competitions)

@competitions_bp.route('/api', methods=['GET', 'POST'])
def api_competitions():
    """API endpoint for competitions"""
    if request.method == 'POST':
        data = request.get_json()
        competition = Competition(
            name=data['name'],
            location=data['location'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            description=data.get('description', '')
        )
        db.session.add(competition)
        db.session.commit()
        return jsonify({'message': 'Competition created successfully', 'id': competition.id}), 201
    
    competitions = Competition.query.all()
    return jsonify([competition.to_dict() for competition in competitions])
