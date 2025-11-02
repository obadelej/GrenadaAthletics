from flask import Blueprint, render_template, request, flash, redirect, url_for
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

@main_bp.route('/about')
def about():
    """About us page"""
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact us page"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Basic validation
        if not all([name, email, subject, message]):
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html')
        
        # In a real application, you would:
        # 1. Send an email using Flask-Mail or similar
        # 2. Store the message in a database
        # 3. Send a confirmation email to the user
        
        # For now, just flash a success message
        flash(f'Thank you {name}! Your message has been received. We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')
