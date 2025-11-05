import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from extensions import db
from app.models.director import Director


directors_bp = Blueprint('directors', __name__)


def _uploads_dir() -> str:
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads', 'directors')
    os.makedirs(base, exist_ok=True)
    return base


@directors_bp.route('/')
def index():
    items = Director.query.order_by(Director.last_name.asc(), Director.first_name.asc()).all()
    return render_template('directors/index.html', items=items)


@directors_bp.route('/<int:item_id>')
def detail(item_id: int):
    item = Director.query.get_or_404(item_id)
    return render_template('directors/detail.html', item=item)


@directors_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        role = request.form.get('role', '').strip()
        bio = request.form.get('bio', '').strip()
        img_file = request.files.get('img')

        if not first_name or not last_name or not role:
            flash('First Name, Last Name, and Role are required.', 'error')
            return redirect(url_for('directors.create'))

        img_path_rel = None
        if img_file and img_file.filename:
            filename = secure_filename(img_file.filename)
            save_dir = _uploads_dir()
            save_path = os.path.join(save_dir, filename)
            img_file.save(save_path)
            img_path_rel = f"uploads/directors/{filename}"

        item = Director(
            first_name=first_name,
            last_name=last_name,
            role=role,
            bio=bio if bio else None,
            img_path=img_path_rel,
        )
        db.session.add(item)
        db.session.commit()
        flash('Director created.', 'success')
        return redirect(url_for('directors.index'))

    return render_template('directors/form.html', item=None)


@directors_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit(item_id: int):
    item = Director.query.get_or_404(item_id)

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        role = request.form.get('role', '').strip()
        bio = request.form.get('bio', '').strip()
        img_file = request.files.get('img')

        if not first_name or not last_name or not role:
            flash('First Name, Last Name, and Role are required.', 'error')
            return redirect(url_for('directors.edit', item_id=item.id))

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
            item.img_path = f"uploads/directors/{filename}"

        item.first_name = first_name
        item.last_name = last_name
        item.role = role
        item.bio = bio if bio else None

        db.session.commit()
        flash('Director updated.', 'success')
        return redirect(url_for('directors.index'))

    return render_template('directors/form.html', item=item)


@directors_bp.route('/<int:item_id>/delete', methods=['POST'])
def delete(item_id: int):
    item = Director.query.get_or_404(item_id)
    
    # Delete image file if it exists
    if item.img_path:
        img_path_full = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', item.img_path)
        if os.path.exists(img_path_full):
            os.remove(img_path_full)
    
    db.session.delete(item)
    db.session.commit()
    flash('Director deleted.', 'success')
    return redirect(url_for('directors.index'))

