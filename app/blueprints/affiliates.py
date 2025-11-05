import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from extensions import db
from app.models.affiliate import Affiliate


affiliates_bp = Blueprint('affiliates', __name__)


def _uploads_dir() -> str:
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads', 'affiliates')
    os.makedirs(base, exist_ok=True)
    return base


@affiliates_bp.route('/')
def index():
    items = Affiliate.query.order_by(Affiliate.team_name.asc()).all()
    return render_template('affiliates/index.html', items=items)


@affiliates_bp.route('/<int:item_id>')
def detail(item_id: int):
    item = Affiliate.query.get_or_404(item_id)
    return render_template('affiliates/detail.html', item=item)


@affiliates_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        team_name = request.form.get('team_name', '').strip()
        team_code = request.form.get('team_code', '').strip()
        team_colors = request.form.get('team_colors', '').strip()
        contact = request.form.get('contact', '').strip()
        email = request.form.get('email', '').strip()
        img_file = request.files.get('img')

        if not team_name or not team_code:
            flash('Team Name and Team Code are required.', 'error')
            return redirect(url_for('affiliates.create'))

        img_path_rel = None
        if img_file and img_file.filename:
            filename = secure_filename(img_file.filename)
            save_dir = _uploads_dir()
            save_path = os.path.join(save_dir, filename)
            img_file.save(save_path)
            img_path_rel = f"uploads/affiliates/{filename}"

        item = Affiliate(
            team_name=team_name,
            team_code=team_code,
            team_colors=team_colors if team_colors else None,
            contact=contact if contact else None,
            email=email if email else None,
            img_path=img_path_rel,
        )
        db.session.add(item)
        db.session.commit()
        flash('Affiliate created.', 'success')
        return redirect(url_for('affiliates.index'))

    return render_template('affiliates/form.html', item=None)


@affiliates_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit(item_id: int):
    item = Affiliate.query.get_or_404(item_id)

    if request.method == 'POST':
        team_name = request.form.get('team_name', '').strip()
        team_code = request.form.get('team_code', '').strip()
        team_colors = request.form.get('team_colors', '').strip()
        contact = request.form.get('contact', '').strip()
        email = request.form.get('email', '').strip()
        img_file = request.files.get('img')

        if not team_name or not team_code:
            flash('Team Name and Team Code are required.', 'error')
            return redirect(url_for('affiliates.edit', item_id=item.id))

        if img_file and img_file.filename:
            # Delete old image if it exists
            if item.img_path:
                old_img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', item.img_path)
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)
            
            filename = secure_filename(img_file.filename)
            save_dir = _uploads_dir()
            save_path = os.path.join(save_dir, filename)
            img_file.save(save_path)
            item.img_path = f"uploads/affiliates/{filename}"

        item.team_name = team_name
        item.team_code = team_code
        item.team_colors = team_colors if team_colors else None
        item.contact = contact if contact else None
        item.email = email if email else None

        db.session.commit()
        flash('Affiliate updated.', 'success')
        return redirect(url_for('affiliates.index'))

    return render_template('affiliates/form.html', item=item)


@affiliates_bp.route('/<int:item_id>/delete', methods=['POST'])
def delete(item_id: int):
    item = Affiliate.query.get_or_404(item_id)
    
    # Delete image file if it exists
    if item.img_path:
        img_path_full = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', item.img_path)
        if os.path.exists(img_path_full):
            os.remove(img_path_full)
    
    db.session.delete(item)
    db.session.commit()
    flash('Affiliate deleted.', 'success')
    return redirect(url_for('affiliates.index'))

