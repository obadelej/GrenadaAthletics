import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, send_file
from extensions import db
from app.models.result import Result


results_bp = Blueprint('results', __name__)


@results_bp.route('/')
def index():
    items = Result.query.order_by(Result.meet_date.desc()).all()
    return render_template('results/index.html', items=items)


@results_bp.route('/pdf/<path:filename>')
def serve_pdf(filename):
    """Serve PDF files from static/results directory"""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    results_dir = os.path.join(project_root, 'static', 'results')
    return send_from_directory(results_dir, filename)


@results_bp.route('/download/<path:filename>')
def download_pdf(filename):
    """Download PDF file with Save As dialog"""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    pdf_path = os.path.join(project_root, 'static', 'results', filename)
    
    if not os.path.exists(pdf_path):
        flash('PDF file not found.', 'error')
        return redirect(url_for('results.index'))
    
    # Get the meet name from the filename or use the filename as default
    # Remove extension for cleaner filename
    download_name = os.path.splitext(filename)[0] + '.pdf'
    
    response = send_file(
        pdf_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=download_name
    )
    
    # Explicitly set headers to force download
    response.headers['Content-Disposition'] = f'attachment; filename="{download_name}"'
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response


@results_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        meet_name = request.form.get('meet_name', '').strip()
        meet_date_str = request.form.get('meet_date', '').strip()
        pdf_filename = request.form.get('pdf_filename', '').strip()
        description = request.form.get('description', '').strip()

        if not meet_name or not meet_date_str or not pdf_filename:
            flash('Meet Name, Meet Date, and PDF Filename are required.', 'error')
            return redirect(url_for('results.create'))

        try:
            meet_date = datetime.strptime(meet_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('results.create'))

        # Verify PDF file exists
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        pdf_path = os.path.join(project_root, 'static', 'results', pdf_filename)
        if not os.path.exists(pdf_path):
            flash(f'PDF file not found: {pdf_filename}. Please ensure the file exists in static/results folder.', 'error')
            return redirect(url_for('results.create'))

        item = Result(
            meet_name=meet_name,
            meet_date=meet_date,
            pdf_filename=pdf_filename,
            description=description if description else None,
        )
        db.session.add(item)
        db.session.commit()
        flash('Result entry created.', 'success')
        return redirect(url_for('results.index'))

    return render_template('results/form.html', item=None)


@results_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit(item_id: int):
    item = Result.query.get_or_404(item_id)

    if request.method == 'POST':
        meet_name = request.form.get('meet_name', '').strip()
        meet_date_str = request.form.get('meet_date', '').strip()
        pdf_filename = request.form.get('pdf_filename', '').strip()
        description = request.form.get('description', '').strip()

        if not meet_name or not meet_date_str or not pdf_filename:
            flash('Meet Name, Meet Date, and PDF Filename are required.', 'error')
            return redirect(url_for('results.edit', item_id=item.id))

        try:
            meet_date = datetime.strptime(meet_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('results.edit', item_id=item.id))

        # Verify PDF file exists (only if filename changed)
        if pdf_filename != item.pdf_filename:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            pdf_path = os.path.join(project_root, 'static', 'results', pdf_filename)
            if not os.path.exists(pdf_path):
                flash(f'PDF file not found: {pdf_filename}. Please ensure the file exists in static/results folder.', 'error')
                return redirect(url_for('results.edit', item_id=item.id))

        item.meet_name = meet_name
        item.meet_date = meet_date
        item.pdf_filename = pdf_filename
        item.description = description if description else None

        db.session.commit()
        flash('Result entry updated.', 'success')
        return redirect(url_for('results.index'))

    return render_template('results/form.html', item=item)


@results_bp.route('/<int:item_id>/delete', methods=['POST'])
def delete(item_id: int):
    item = Result.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Result entry deleted.', 'success')
    return redirect(url_for('results.index'))

