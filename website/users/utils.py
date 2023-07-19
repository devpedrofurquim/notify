from .. import mail
import os
from PIL import Image
import secrets
from flask import url_for, current_app
from flask_mail import Message

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset Your Password', sender='notify344@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_page', token=token, _external=True)}
        
If you did not make this request then simply ignore this email.
'''
    mail.send(msg)
    
def delete_picture(filename):
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)

    os.remove(picture_path)
    return True
    
def save_picture(picture, user):
    if user.image_file != 'default.png':
        delete_picture(user.image_file) 
    
    print(user.image_file)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
    
    output_size = (240, 240)
    # Resises picture to 240x240
    i = Image.open(picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    
    return picture_filename