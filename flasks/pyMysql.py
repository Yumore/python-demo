import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='username',
        password='password',
        database='dbname',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    email = data['email']

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO user (username, email) VALUES (%s, %s)', (name, email))
        connection.commit()

    connection.close()
    return 'User added!'


@app.route('/get_users')
def get_users():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()

    connection.close()
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
