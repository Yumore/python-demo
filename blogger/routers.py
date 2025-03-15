from flask import Blueprint, render_template

blog = Blueprint('blogger', __name__)


@blog.route('/')
def index():
    return render_template('index.html')


@blog.route('/post/<int:post_id>')
def post(post_id):
    return f'Post ID: {post_id}'


@blog.errorhandler(404)
def page_not_found(error):
    return 'Page not found', 404
