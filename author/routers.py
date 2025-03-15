from flask import Blueprint, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from author.custom_error import CustomError
from flasks.user import User

auth = Blueprint('author', __name__)
# 使用 SQLite 数据库
# auth.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# auth.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(auth)
# 创建数据库
with auth.app_context_processor:
    db.create_all()


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return redirect(url_for('author.login'))


@auth.route('/register')
def register():
    return render_template('register.html')


@auth.route('/add_user')
def add_user():
    new_user = User(username='john_doe', email='john@example.com')
    db.session.add(new_user)
    db.session.commit()
    return 'User added!'


@auth.route('/get_users')
def get_users():
    users = User.query.all()  # 获取所有用户
    return '<br>'.join([f'{user.username} ({user.email})' for user in users])


@auth.route('/update_user/<int:user_id>')
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.username = 'new_username'
        db.session.commit()
        return 'User updated!'
    return 'User not found!'


@auth.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'User deleted!'
    return 'User not found!'


@auth.route('/raw_sql')
def raw_sql():
    result = db.session.execute('SELECT * FROM user')
    return '<br>'.join([str(row) for row in result])


@auth.before_app_request
def before_request():
    # 执行在每个请求之前的操作
    pass


@auth.after_app_request
def after_request(response):
    # 执行在每个请求之后的操作
    return response


@auth.errorhandler(404)
def auth_not_found(error):
    return render_template('auth_404.html'), 404


# 抛异常
@auth.route('/raise_custom_error')
def raise_custom_error():
    raise CustomError("This is a custom error.")


# 处理异常
@auth.errorhandler(CustomError)
def handle_custom_error(error):
    return str(error), 400
