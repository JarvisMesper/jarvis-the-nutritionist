from flask import Flask, jsonify
from RequestOpenFood import RequestOpenFood
from RequestOpenFood import QuerryError
from RequestOpenFood import ProductBuilder

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getnames/<string:code>")
def getnames(code):
    try:
        tags = code.split('-')
        res = RequestOpenFood.search_name(id_from=0, id_size=5, name=tags)
        res = ProductBuilder.clean_data(res)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])
    
@app.route("/getingredients/<string:code>")
def getingredients(code):
    try:
        tags = code.split('-')
        res = RequestOpenFood.search_ingredient(id_from=0, id_size=5, name=tags)
        res = ProductBuilder.clean_data(res)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])

@app.route("/getbarcode/<string:code>")
def get_barcode(code):
    try:
        res = RequestOpenFood.get_product(barcode=code)
        res = ProductBuilder.clean_data(res)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])
 
if __name__ == "__main__":
    app.run()

