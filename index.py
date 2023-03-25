from flask import Flask, request, jsonify
import json

app = Flask(__name__)

items = [
    {"name":"iphone", "category":1, "price":20.5, "instock":200},
    {"name":"samsung", "category":2, "price":15.5, "instock":300},
]

def _find_next_name(name):
    data = [x for x in items if x['name'] == name]
    return data

#GET - REST API
@app.route('/items', methods=["GET"])
def get_item():
    return jsonify(items)

#GET - by name
@app.route('/items/<name>', methods=["GET"])
def get_items_name(name):
    data = _find_next_name(name)
    return jsonify(data)

def get_items(name):
  return next((e for e in items if e['name'] == name), None)

@app.route('/items/<name>', methods=["DELETE"])
def delete_item(name: str):

    data = _find_next_name(name)
    if not data:
        return {"ERROR": "Items does not exist."}, 404
    else:
        items.remove(data[0])
        return "Items deleted successfully.", 200

def items_is_valid(data):
  for key in data.keys():
    if key != 'name':
      return False
  return True

@app.route('/items', methods=["POST"])
def post_items():
    name = request.form.get('name')
    category = request.form.get('category')
    price = request.form.get('price')
    instock = request.form.get('instock')

    new_data = {
        "name": name,
        "category": category,
        "price": price,
        "instock":instock,
    }

    if (_find_next_name(name) == name):
        return {"ERROR": "Bad Request."}, name
    else:
        items.append(new_data)
        return jsonify(items)

@app.route('/items/<name>', methods=['PUT'])
def update_items(name):
    items = get_items(name)
    if items is None:
        return jsonify({ 'ERROR': 'Items does not Exist.'}), 404
    
    updated_items = json.loads(request.data)
    if not items_is_valid(updated_items):
        return jsonify({ 'ERROR': 'Invalid items properties.'})
    
    items.update(updated_items)

    return jsonify(items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)