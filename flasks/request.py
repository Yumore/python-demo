from index import app


@app.route('/submit', methods=['POST'])
def submit():
    return 'Form submitted!'
