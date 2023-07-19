import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from website.models import Note, User
from flask_login import login_user, login_required, logout_user, current_user
from . import db, app, mail
from sqlalchemy import desc
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
import json

views = Blueprint('views', __name__)