from flask import Blueprint, render_template
from flask_login import current_user


articles = Blueprint('articles', __name__)

Articles = {
    1: {
        'article_subject': 'creativity',
        'article_title': 'Embracing Creativity: Unleash the Power of Imagination',
        'article_content': "In a world that thrives on innovation and originality, creativity stands as the driving force behind some of the most groundbreaking ideas and inventions. From art and literature to technology and science, creativity paves the way for progress and pushes the boundaries of human capability Creativity is not an elusive trait reserved for a chosen few; it resides within each of us, waiting to be unleashed. Often, people underestimate their creative potential, believing that creativity is a gift bestowed upon a select few. However, the truth is that creativity can be cultivated and nurtured like a skill.",
        'article_image': 'creativity.jpg',
        'article_author': 'Pedro Furquim'
    },
    2: {
        'article_subject': 'organization',
        'article_title': 'Harnessing the Art of Organization: From Chaos to Clarity',
        'article_content': "In the fast-paced world we live in, the ability to stay organized is a superpower. It's not merely about neat desks and color-coded calendars; organization is the key to unlocking your productivity and maintaining a sense of control over your life.",
        'article_image': 'organization.jpg',
        'article_author': 'Pedro Furquim'
    }
}

@articles.route('/article/<string:article_subject>')
def article(article_subject):
    return render_template('article.html', article_subject=article_subject, articles=Articles, user=current_user)
