import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from extensions import db
from app.models.news import News


news_bp = Blueprint('news', __name__)


def _uploads_dir() -> str:
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads', 'news')
    os.makedirs(base, exist_ok=True)
    return base


@news_bp.route('/')
def index():
    items = News.query.order_by(News.date_created.desc()).all()
    return render_template('news/index.html', items=items)


@news_bp.route('/<int:item_id>')
def detail(item_id: int):
    item = News.query.get_or_404(item_id)
    return render_template('news/detail.html', item=item)


@news_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        date_created_str = request.form.get('date_created', '').strip()
        photo_file = request.files.get('photo')

        if not title or not author or not content:
            flash('Title, Author, and Content are required.', 'error')
            return redirect(url_for('news.create'))

        date_created = None
        if date_created_str:
            try:
                date_created = datetime.fromisoformat(date_created_str)
            except ValueError:
                flash('Invalid date format. Use YYYY-MM-DD or leave blank.', 'error')
                return redirect(url_for('news.create'))

        photo_path_rel = None
        if photo_file and photo_file.filename:
            filename = secure_filename(photo_file.filename)
            save_dir = _uploads_dir()
            save_path = os.path.join(save_dir, filename)
            photo_file.save(save_path)
            photo_path_rel = f"uploads/news/{filename}"

        item = News(
            title=title,
            author=author,
            content=content,
            date_created=date_created or datetime.utcnow(),
            photo_path=photo_path_rel,
        )
        db.session.add(item)
        db.session.commit()
        flash('News item created.', 'success')
        return redirect(url_for('news.index'))

    return render_template('news/form.html', item=None)


@news_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit(item_id: int):
    item = News.query.get_or_404(item_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()
        date_created_str = request.form.get('date_created', '').strip()
        photo_file = request.files.get('photo')

        if not title or not author or not content:
            flash('Title, Author, and Content are required.', 'error')
            return redirect(url_for('news.edit', item_id=item.id))

        if date_created_str:
            try:
                item.date_created = datetime.fromisoformat(date_created_str)
            except ValueError:
                flash('Invalid date format. Use YYYY-MM-DD.', 'error')
                return redirect(url_for('news.edit', item_id=item.id))

        if photo_file and photo_file.filename:
            filename = secure_filename(photo_file.filename)
            save_dir = _uploads_dir()
            save_path = os.path.join(save_dir, filename)
            photo_file.save(save_path)
            item.photo_path = f"uploads/news/{filename}"

        item.title = title
        item.author = author
        item.content = content

        db.session.commit()
        flash('News item updated.', 'success')
        return redirect(url_for('news.index'))

    return render_template('news/form.html', item=item)


@news_bp.route('/<int:item_id>/delete', methods=['POST'])
def delete(item_id: int):
    item = News.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('News item deleted.', 'success')
    return redirect(url_for('news.index'))


