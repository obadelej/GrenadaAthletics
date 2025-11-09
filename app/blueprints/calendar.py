import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from app.models.calendar import Calendar

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


calendar_bp = Blueprint('calendar', __name__)


@calendar_bp.route('/')
def index():
    # Get filter parameters
    start_date_filter = request.args.get('start_date', '')
    end_date_filter = request.args.get('end_date', '')
    
    # Build query
    query = Calendar.query
    
    if start_date_filter:
        try:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
            query = query.filter(Calendar.start_date >= start_date)
        except ValueError:
            pass
    
    if end_date_filter:
        try:
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d').date()
            query = query.filter(Calendar.end_date <= end_date)
        except ValueError:
            pass
    
    items = query.order_by(Calendar.start_date.asc()).all()
    
    return render_template('calendar/index.html', 
                         items=items, 
                         start_date_filter=start_date_filter,
                         end_date_filter=end_date_filter)


@calendar_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        start_date_str = request.form.get('start_date', '').strip()
        end_date_str = request.form.get('end_date', '').strip()
        activity = request.form.get('activity', '').strip()
        venue = request.form.get('venue', '').strip()

        if not start_date_str or not end_date_str or not activity:
            flash('Start Date, End Date, and Activity are required.', 'error')
            return redirect(url_for('calendar.create'))

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            if start_date > end_date:
                flash('Start date must be before or equal to end date.', 'error')
                return redirect(url_for('calendar.create'))
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('calendar.create'))

        item = Calendar(
            start_date=start_date,
            end_date=end_date,
            activity=activity,
            venue=venue if venue else None,
        )
        db.session.add(item)
        db.session.commit()
        flash('Calendar entry created.', 'success')
        return redirect(url_for('calendar.index'))

    return render_template('calendar/form.html', item=None)


@calendar_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit(item_id: int):
    item = Calendar.query.get_or_404(item_id)

    if request.method == 'POST':
        start_date_str = request.form.get('start_date', '').strip()
        end_date_str = request.form.get('end_date', '').strip()
        activity = request.form.get('activity', '').strip()
        venue = request.form.get('venue', '').strip()

        if not start_date_str or not end_date_str or not activity:
            flash('Start Date, End Date, and Activity are required.', 'error')
            return redirect(url_for('calendar.edit', item_id=item.id))

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            if start_date > end_date:
                flash('Start date must be before or equal to end date.', 'error')
                return redirect(url_for('calendar.edit', item_id=item.id))
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('calendar.edit', item_id=item.id))

        item.start_date = start_date
        item.end_date = end_date
        item.activity = activity
        item.venue = venue if venue else None

        db.session.commit()
        flash('Calendar entry updated.', 'success')
        return redirect(url_for('calendar.index'))

    return render_template('calendar/form.html', item=item)


@calendar_bp.route('/<int:item_id>/delete', methods=['POST'])
def delete(item_id: int):
    item = Calendar.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Calendar entry deleted.', 'success')
    return redirect(url_for('calendar.index'))


@calendar_bp.route('/import', methods=['POST'])
def import_excel():
    """Import calendar data from Excel file"""
    if not PANDAS_AVAILABLE:
        flash('Pandas library is required for Excel import. Please install it: pip install pandas openpyxl', 'error')
        return redirect(url_for('calendar.index'))
    
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    excel_path = os.path.join(project_root, 'static', 'docs', 'calendar.xlsx')
    
    if not os.path.exists(excel_path):
        flash(f'Excel file not found at {excel_path}', 'error')
        return redirect(url_for('calendar.index'))
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_path, engine='openpyxl')
        
        # Clear existing data (optional - you might want to keep existing and append)
        # Calendar.query.delete()
        # db.session.commit()
        
        # Expected columns: start_date, end_date, activity, venue
        # Map column names (case-insensitive)
        column_map = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if 'start' in col_lower and 'date' in col_lower and 'start_date' not in column_map:
                column_map['start_date'] = col
            elif 'end' in col_lower and 'date' in col_lower and 'end_date' not in column_map:
                column_map['end_date'] = col
            elif ('activity' in col_lower or 'event' in col_lower or 'description' in col_lower) and 'activity' not in column_map:
                column_map['activity'] = col
            elif ('venue' in col_lower or 'location' in col_lower) and 'venue' not in column_map:
                column_map['venue'] = col
        
        if 'start_date' not in column_map or 'end_date' not in column_map or 'activity' not in column_map:
            flash('Excel file must contain columns for start_date, end_date, and activity.', 'error')
            return redirect(url_for('calendar.index'))
        
        imported_count = 0
        errors = []
        
        for idx, row in df.iterrows():
            try:
                start_date = pd.to_datetime(row[column_map['start_date']]).date()
                end_date = pd.to_datetime(row[column_map['end_date']]).date()
                activity = str(row[column_map['activity']]).strip()
                
                if pd.isna(activity) or not activity:
                    continue
                
                venue = None
                if 'venue' in column_map:
                    venue_val = row[column_map['venue']]
                    if not pd.isna(venue_val):
                        venue = str(venue_val).strip()
                
                # Check if entry already exists (optional - skip duplicates)
                existing = Calendar.query.filter_by(
                    start_date=start_date,
                    end_date=end_date,
                    activity=activity
                ).first()
                
                if existing:
                    continue
                
                item = Calendar(
                    start_date=start_date,
                    end_date=end_date,
                    activity=activity,
                    venue=venue,
                )
                db.session.add(item)
                imported_count += 1
            except Exception as e:
                errors.append(f"Row {idx + 2}: {str(e)}")
                continue
        
        db.session.commit()
        
        if imported_count > 0:
            flash(f'Successfully imported {imported_count} calendar entries.', 'success')
        else:
            flash('No new entries were imported. They may already exist.', 'info')
        
        if errors:
            flash(f'Some rows had errors: {"; ".join(errors[:5])}', 'warning')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error importing Excel file: {str(e)}', 'error')
    
    return redirect(url_for('calendar.index'))

