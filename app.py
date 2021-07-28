from flask import Flask, jsonify, request

app = Flask(__name__) # Esta es mi aplicacion de servidor

from products import products

@app.route('/ping') # Cada vez que alguien visite esta ruta se va a ejecutar la funcion
def ping():
    return jsonify({'message': 'Pong'})

@app.route('/products') # Por defecto las rutas usan el metodo GET
def getProducts():
    return jsonify({'products': products})

@app.route('/products/<string:product_name>') # Para que me devuelva solo el JSON de un producto que solicite
def getProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]

    if len(productsFound) > 0:
        return jsonify({'product': productsFound[0]})

    return jsonify({"message": 'Product not found'})

@app.route('/products', methods=['POST']) # A pesar que se tiene la misma ruta /products, van a estar funcionando
                                        # con diferentes metodos HTTP entonces no hay problema
def addProduct():
    # print(request.json) # Imprime el json que me enviaron al hacer POST en la API
    newProduct = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }

    products.append(newProduct)

    return jsonify({"message": "product added succesfully!", "products": products})

@app.route('/products/<string:product_name>', methods=['PUT']) # Para actualizar valores
def editProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']

        return jsonify({
            "message": "Product updated",
            "product": productsFound[0]
        }) # Si llamo el metodo GET products debera aparecer el JSON actualizado

    return jsonify({"message": "Product not found"})

@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            "message": "Product deleted",
            "products": products
        })
    
    return jsonify({"message": "Product not found"})

if __name__ == '__main__':
    app.run(debug=True, port=4000)