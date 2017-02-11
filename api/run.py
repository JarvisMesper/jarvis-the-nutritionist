from flask import Flask, jsonify
from RequestOpenFood import RequestOpenFood
from RequestOpenFood import QuerryError
from RequestOpenFood import ProductBuilder
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

@app.route("/getimage/<string:code>")
def get_image(code):
    print("Getting image")
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot([0,1],[1,2])

    canvas=FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    return png_output.getvalue()

@app.route("/getbarcode/<string:code>")
def get_barcode(code):
    print("Getting barcode" + code)
    try:
        res = RequestOpenFood.get_product(barcode=code)
        res = ProductBuilder.clean_data(res)
        return jsonify(data=res)
    except QuerryError as err:
        return jsonify(data=[])
 
if __name__ == "__main__":
    app.run(host='0.0.0.0')

