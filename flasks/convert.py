from index import app


@app.route('/items/<int:item_id>/details')
def item_details(item_id):
    return f'Item details for item ID: {item_id}'
