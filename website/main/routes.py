from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .. import db
from website.models import Note, User
from sqlalchemy import desc

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
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
    
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of notes to display per page
    user = User.query.get(current_user.id)
    notes = Note.query.filter_by(user_id=user.id).order_by(desc(Note.date)).paginate(page=page, per_page=per_page)    
    
    return render_template('home.html',user=current_user, notes=notes)
