from flask import Blueprint, render_template
from app.models import Athlete, Event, Competition

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    athletes_count = Athlete.query.count()
    events_count = Event.query.count()
    competitions_count = Competition.query.count()
    
    return render_template('index.html', 
                         athletes_count=athletes_count,
                         events_count=events_count,
                         competitions_count=competitions_count)
