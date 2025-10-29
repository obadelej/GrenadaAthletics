from flask import Blueprint, render_template, request, jsonify, flash
from app.models import Athlete
from extensions import db

athletes_bp = Blueprint('athletes', __name__)

@athletes_bp.route('/')
def athletes():
    """Athletes page"""
    athletes = Athlete.query.all()
    return render_template('athletes.html', athletes=athletes)

@athletes_bp.route('/api', methods=['GET', 'POST'])
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
    return jsonify([athlete.to_dict() for athlete in athletes])
