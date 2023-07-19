from sqlalchemy import or_
from .utils import send_reset_email, save_picture
from flask import Blueprint,render_template, request, flash, redirect, url_for
from .. import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user

users = Blueprint('users', __name__)

@users.route("/getTime", methods=['GET'])
def getTime():
    time = request.args.get('time')
    return time

@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(or_(User.email == email, User.username == username)).first()

        if user:
            if user.email == email:
                flash('Email already exists.', category='error')
            if user.username == username:
                flash('Username already exists.', category='error')
        elif len(email) < 4: 
            flash('Email must be greater than 3 characters.', category='error')
        elif len(email) > 99:
            flash('Email must be shorter than 100 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif len(username) > 10:
            flash('Username must be shorter than 10 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(password1) > 15:
            flash('Password must be shorter than 15 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('main.home'))

    return render_template("register.html", user=current_user)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember-me')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=bool(remember))
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        picture = request.files.get('picture', '')
        

        if email:
            if User.query.filter(User.email == email).filter(User.id != current_user.id).first():
                flash('Email already taken.', category='error')
            elif email == current_user.email:
                flash('Email already set.', category='error')
            else:
                if len(email) < 4:
                    flash('Email must be greater than 3 characters.', category='error')
                elif len(email) > 99:
                    flash('Email must be shorter than 100 characters.', category='error')
                else:
                    current_user.email = email
                    db.session.commit()
                    flash('Email updated.', category='success')


        if username:
            if User.query.filter(User.username == username).filter(User.id != current_user.id).first():
                flash('Username already taken.', category='error')
            elif username == current_user.username:
                flash('Username already set.', category='error')
            else:
                if len(username) < 2:
                    flash('Username must be greater than 1 character.', category='error')
                elif len(username) > 10:
                    flash('Username must be shorter than 11 characters.', category='error')
                else:
                    current_user.username = username
                    db.session.commit()
                    flash('Username updated.', category='success')
  
        if picture:
            picture_file = save_picture(picture, current_user)
            current_user.image_file = picture_file
            db.session.commit()
            flash('Picture updated.', category='success')



        
        return redirect(url_for('users.profile'))

    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("profile.html", user=current_user, img_file = img_file)

@users.route('/request', methods=['GET', 'POST'])
def request_page():
    if request.method == 'POST':
        
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('If an account with this email address exists, a password reset message will be sent shortly.', category="sucess")

        #Send Email to user
        send_reset_email(user) 
        flash('If an account with this email address exists, a password reset message will be sent shortly.', category="sucess")
        return redirect(url_for('users.login'))
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    return render_template('request.html', user=current_user)

@users.route('/reset-<token>', methods=['GET', 'POST'])
def reset_page(token):
    
    user = User.verify_reset_token(token)

    
    if request.method == 'POST':
        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(password1) > 15:
            flash('Password must be shorter than 15 characters.', category='error')
        else:
            hashed_password = generate_password_hash(
                    password1, method='scrypt')
            user.password = hashed_password
            db.session.commit()
            login_user(user, remember=True)
            flash('Password updated successfully', category='success')
            return redirect(url_for('main.home'))
            
    if user is None:
        flash('If an account with this email address exists, a password reset message will be sent shortly.', category="sucess")

            
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))    
    
    if user is None:
        flash('Invalid or Expired Token', category='error')
        return redirect(url_for('users.request_page'))
    
    return render_template('reset.html', user=current_user)