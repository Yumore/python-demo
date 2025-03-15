from index import app


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'User ID: {user_id}'


@app.route('/files/<path:filename>')
def serve_file(filename):
    return f'Serving file: {filename}'
