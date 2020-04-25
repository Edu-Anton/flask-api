from flask import Flask, jsonify, request
# jsonify permite convertir un objeto a json reconocido por el navegador

app = Flask(__name__)

from products import products

@app.route('/ping')
def ping():
  return jsonify({"message":"Pong"})

@app.route('/products', methods=['GET'])
def getProducts():
  # Una forma
  # return jsonify(products)
  # Otra forma con nombre, con mensaje. Puedo enviar todos los datos
  return jsonify({"products": products, "message": "Product´s List"})

@app.route('/products/<string:product_name>')
def getProduct(product_name):
  productFound = [product for product in products if product['name'] == product_name]
  if (len(productFound) > 0):
    return jsonify({"product":productFound[0]})
  return jsonify({"message": "Product not found"})

@app.route('/products', methods=['POST'])
def addProduct():
  new_product = {
    "name": request.json['name'],
    "price": request.json['price'],
    "quantity": request.json['quantity']
  }
  products.append(new_product)
  return jsonify({"message":"Producto agregado satisfactoriamente", "products":products})

@app.route('/products/<product_name>', methods=['PUT'])
def editProduct(product_name):
  productFound = [product for product in products if product['name'] == product_name]
  if (len(productFound) > 0):
    productFound[0]['name'] = request.json['name']
    productFound[0]['price'] = request.json['price']
    productFound[0]['quantity'] = request.json['quantity']
    return jsonify({
      "message": "Product Updated",
      "product": productFound[0]
    })

@app.route('/products/<product_name>', methods=['DELETE'])
def deleteProduct(product_name):
  productFound = [product for product in products if product['name'] == product_name]
  if (len(productFound) > 0):
    products.remove(productFound[0])
    return jsonify({
      "message": "Product Deleted",
      "products": products
    })
  return jsonify({"message": "Product Not Found"})

if __name__ == '__main__':
  app.run(debug=True, port=3000)