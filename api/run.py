from flask import Flask, jsonify
from RequestOpenFood import RequestOpenFood
from RequestOpenFood import QuerryError
from RequestOpenFood import ProductBuilder
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Flask(__name__)

@app.route("/")
def hello():
    print("Hello World!")
    return "Hello World!"

@app.route("/getnames/<string:code>")
def getnames(code):
    print("Getting name from code")
    try:
        tags = code.split('-')
        res = RequestOpenFood.search_name(id_from=0, id_size=5, name=tags)
        res = ProductBuilder.clean_data(res)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])

@app.route("/getingredients/<string:code>")
def getingredients(code):
    print("Getting ingredients")
    try:
        tags = code.split('-')
        res = RequestOpenFood.search_ingredient(id_from=0, id_size=5, name=tags)
        res = ProductBuilder.clean_data(res)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])

@app.route("/comparaison/<string:code>")
def comparaison(code):
    res = RequestOpenFood.get_product(barcode='7610235000329')
    res = ProductBuilder.clean_data(res)
    res2 = RequestOpenFood.get_product(barcode='7613033774188')
    res2 = ProductBuilder.clean_data(res2)
    return RequestOpenFood.compare_data(res[0], res2[0])

@app.route("/getbarcode/<string:code>")
def get_barcode(code):
    print("Getting barcode" + code)
    try:
        res = RequestOpenFood.get_product(barcode=code)
        res = ProductBuilder.clean_data(res)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])

@app.route("/product-contains/<string:code>")
def get_contains(code):
    print("Getting containing" + code)
    try:
        product = code.split("-")[0]
        ingredient = code.split("-")[1]
        res = RequestOpenFood.is_containing_ingredient(product, ingredient)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])

if __name__ == "__main__":
    app.run(host='0.0.0.0')

