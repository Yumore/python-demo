import glob
import os

from flask import Flask, render_template, abort

from middleware import CustomMiddleware

# 导入蓝图
app = Flask(__name__)

# 注册蓝图
# app.register_blueprint(auth, url_prefix='/author')
# app.register_blueprint(blog, url_prefix='/blogger')

app.wsgi_app = CustomMiddleware(app.wsgi_app)

ROOT_PATH = os.path.expanduser('~/workspace')
LOG_FILE = os.path.join(ROOT_PATH, 'update-git.log')

# 查找所有git仓库(包含.git的目录)，并且按照字母降序排序(A->Z --> a->z)
git_dirs = glob.glob(os.path.join(ROOT_PATH, '**', '.git'), recursive=True)
git_dirs.sort(reverse=True)


@app.route('/')
def home():
    return render_template('index.html', title='Welcome Page', name='Nathaniel', items=git_dirs)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.route('/profile/<username>')
def profile(username):
    user = {
        'name': username,
        'age': 30,
        'hobbies': ['阅读', '旅行', '编程']
    }
    return render_template('profile.html', user=user)


@app.route('/abort_example')
def abort_example():
    abort(403)  # 返回 403 Forbidden 错误


@app.before_request
def before_request():
    print('Before request')


@app.after_request
def after_request(response):
    print('After request')
    return response


@app.teardown_request
def teardown_request(exception):
    print('Teardown request')


if __name__ == '__main__':
    app.run(debug=True)
