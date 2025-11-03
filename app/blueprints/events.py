from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.event import Event
from extensions import db


events_bp = Blueprint('events', __name__)


@events_bp.route('/')
def events():
    items = Event.query.order_by(Event.event_id.asc()).all()
    return render_template('events/index.html', items=items)


@events_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        event_code = request.form.get('event_code', '').strip()
        event_description = request.form.get('event_description', '').strip()

        if not event_name or not event_code:
            flash('Event name and code are required.', 'error')
            return redirect(url_for('events.create'))

        item = Event(event_name=event_name, event_code=event_code, event_description=event_description)
        db.session.add(item)
        db.session.commit()
        flash('Event created.', 'success')
        return redirect(url_for('events.events'))

    return render_template('events/form.html', item=None)


@events_bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
def edit(event_id: int):
    item = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        event_code = request.form.get('event_code', '').strip()
        event_description = request.form.get('event_description', '').strip()

        if not event_name or not event_code:
            flash('Event name and code are required.', 'error')
            return redirect(url_for('events.edit', event_id=item.event_id))

        item.event_name = event_name
        item.event_code = event_code
        item.event_description = event_description
        db.session.commit()
        flash('Event updated.', 'success')
        return redirect(url_for('events.events'))

    return render_template('events/form.html', item=item)


@events_bp.route('/<int:event_id>/delete', methods=['POST'])
def delete(event_id: int):
    item = Event.query.get_or_404(event_id)
    db.session.delete(item)
    db.session.commit()
    flash('Event deleted.', 'success')
    return redirect(url_for('events.events'))
