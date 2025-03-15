import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='username',
        password='password',
        database='dbname'
    )
    return connection


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    email = data['email']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO user (username, email) VALUES (%s, %s)', (name, email))
    connection.commit()
    cursor.close()
    connection.close()

    return 'User added!'


@app.route('/get_users')
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
