from flask import Flask, jsonify
from RequestOpenFood import RequestOpenFood
from RequestOpenFood import QuerryError

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getbarcode/<string:code>")
def get_barcode(code):
	try:
		res = RequestOpenFood.get_product(barcode=code)
		return RequestOpenFood.get_valid_name(res)
	except QuerryError as err:
		return 'Error: ' + err.message
#	return jsonify(data=res)

if __name__ == "__main__":
    app.run()

