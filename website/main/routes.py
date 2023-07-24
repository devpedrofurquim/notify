from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .. import db
from website.models import Note, User
from sqlalchemy import desc

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def foo():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('foo.html', user=current_user)


@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_text = request.form.get('note')
        
        
        if note_text is None:
            return render_template("home.html", user=current_user)
        elif len(note_text) < 1:    
            flash('Note is too short!', category='error')
        else:
            note_text = Note(text=note_text, user_id=current_user.id)
            db.session.add(note_text)
            db.session.commit()
            flash('Note added!', category='success')
            
    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of notes to display per page
    user = User.query.get(current_user.id)
    notes = Note.query.filter_by(user_id=user.id).order_by(desc(Note.date)).paginate(page=page, per_page=per_page)    
    num_notes = Note.query.filter_by(user_id=user.id).count()
    return render_template('home.html',user=current_user, notes=notes, img_file=img_file, num_notes=num_notes)
