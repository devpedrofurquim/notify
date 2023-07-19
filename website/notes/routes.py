from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.models import Note, User
from sqlalchemy import desc
from .. import db
import json

notes =  Blueprint('notes', __name__)

@notes.route('/<int:note_id>', methods=['GET', 'POST'])
@login_required
def note(note_id):
    user = User.query.get(current_user.id)
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note=note, user=current_user)

@notes.route('/edit-note', methods=['POST'])
def edit_note():
    user = User.query.get(current_user.id)
    note_id = request.form.get('noteId')
    note = Note.query.get_or_404(note_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of notes to display per page

    new_text = request.form.get('edit_note')

    notes = Note.query.filter_by(user_id=user.id).order_by(desc(Note.date)).paginate(page=page, per_page=per_page)    


    if note:
        note.text = new_text
        db.session.commit()
        flash('Note edited!', category='success')
        return render_template("home.html", notes=notes, user=current_user)
    else:
        return render_template("home.html", notes=notes, user=current_user)

@notes.route('/delete-note', methods=['POST'])
def delete_note():
    note_data = json.loads(request.data)
    note_id = note_data['noteId']
    note = Note.query.get(note_id)
    
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted!', category='success')
    
    return jsonify({})