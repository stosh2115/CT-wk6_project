from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required 

# internal import
from pokemon_shop.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema 


api = Blueprint('api', __name__, url_prefix='/api') 


@api.route('/token', methods=['GET', 'POST'])
def token():
    
    data = request.json 
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id. Try Again.'
        }
    

@api.route('/shop')
@jwt_required()
def get_shop():
    allprods = Product.query.all()

    response = products_schema.dump(allprods)

    return jsonify(response)


@api.route('/order/create/<cust_id>', methods=['POST']) 
@jwt_required()
def create_order(cust_id):
    
    data = request.json 
    
    customer_order = data['order'] 
    
    customer = Customer.query.filter(Customer.cust_id == cust_id).first() 
    if not customer:
        customer = Customer(cust_id) 
        db.session.add(customer)
        
    order = Order() 
    db.session.add(order)
    
    
    for product in customer_order:
        
        # def __init__(self, prod_id, quantity, price, order_id, cust_id):
        prodorder = ProdOrder(product['prod_id'], product['type'], product['ability'], order.order_id, cust_id)
        db.session.add(prodorder)
        
        #for each product we add to our order we need to increment our order_total
        order.increment_ordertotal(prodorder.price)
        
        #for each product we need to decrement the total quantity available
        current_product = Product.query.get(product['prod_id'])
        current_product.decrement_quantity(product['type'])
        
    db.session.commit()
    
    return {
        'status': 200,
        'message': 'New Order was Created'
    }


@api.route('/order/<cust_id>')
@jwt_required()
def get_orders(cust_id):
    
    # grab all prodorders associated with that customer
    prodorder = ProdOrder.query.filter(ProdOrder.cust_id == cust_id).all()
    
    
    data = []
    
    for order in prodorder:
        
        product = Product.query.filter(Product.prod_id == order.prod_id).first()
        
        product_dict = product_schema.dump(product)
        
        product_dict['quantity'] = order.quantity 
        product_dict['order_id'] = order.order_id 
        product_dict['id'] = order.prodorder_id 
        
        data.append(product_dict)
        
    return jsonify(data)


@api.route('/order/update/<order_id>', methods = ['PUT']) 
@jwt_required()
def update_order(order_id):
    
    data = request.json
    new_quantity = int(data['quantity'])
    prod_id = data['prod_id']
    
    
    # grab all the right objects in our database, Product, ProdOrder, Order
    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first() 
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)
    
    
    order.decrement_ordertotal(prodorder.price) 
    
    prodorder.set_price(product.price, new_quantity)
    
    order.increment_ordertotal(prodorder.price)  
    
    diff = abs(new_quantity - prodorder.quantity)
    
    if prodorder.quantity > new_quantity:
        product.increment_quantity(diff) 
    else:
        product.decrement_quantity(diff) 
        
    prodorder.update_quantity(new_quantity)
    
    db.session.commit()
    
    return {
        'status': 200,
        'message': 'Order was Updated Successfully'
    }



@api.route('/order/delete/<order_id>', methods = ['DELETE'])
@jwt_required()
def delete_order(order_id):

    data = request.json
    prod_id = data['prod_id']


    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)


    order.decrement_ordertotal(prodorder.price) 
    product.increment_quantity(prodorder.quantity) 

    db.session.delete(prodorder)
    db.session.commit()

    return {
        'status' : 200,
        'message': 'Order was Deleted Successfully'
    }