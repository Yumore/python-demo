from index import app


@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'
