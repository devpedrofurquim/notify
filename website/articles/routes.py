from flask import Blueprint, render_template
from flask_login import current_user


articles = Blueprint('articles', __name__)

article_title = 'hello'

@articles.route('/article/<string:article_title>')
def article(article_title):
    return render_template('article.html', article_title=article_title, user=current_user)
