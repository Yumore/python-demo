from index import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def index():
    users = User.query.all()
    return '<br>'.join([f'{user.username} ({user.email})' for user in users])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建数据库表
    app.run(debug=True)
