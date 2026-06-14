import json
from flask import Flask, request, jsonify, session
import products_dao
import uom_dao
import order_dao
import admin_dao
from sql_connection import get_sql_connection
from flask_cors import CORS
import inventory_dao
import analytics_dao
import secrets
secrets.token_hex(32)

app = Flask(__name__)
# Add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

CORS(app)

# Configure session
app.secret_key = 'your_secret_key_change_this_in_production'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours in seconds

app.secret_key = 'change_this_to_random_value'

@app.route('/signup', methods=['POST'])
def signup():
    try:
        request_payload = json.loads(request.form['data'])
        
        # Validate input
        if not request_payload.get('username') or not request_payload.get('email') or not request_payload.get('password'):
            response = jsonify({'error': 'Username, email, and password are required'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        # Check password length
        if len(request_payload['password']) < 6:
            response = jsonify({'error': 'Password must be at least 6 characters'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        result = admin_dao.signup_admin(get_sql_connection(), request_payload)
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        
        if result['success']:
            return response, 201
        else:
            return response, 400
    
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/signin', methods=['POST'])
def signin():
    try:
        request_payload = json.loads(request.form['data'])
        
        # Validate input
        if not request_payload.get('username') or not request_payload.get('password'):
            response = jsonify({'error': 'Username/email and password are required'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        result = admin_dao.signin_admin(get_sql_connection(), request_payload['username'], request_payload['password'])
        
        if result['success']:
            # Store admin info in session
            session['admin_id'] = result['admin_id']
            session['username'] = result['username']
            session.permanent = True
            
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200
        else:
            response = jsonify(result)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 401
    
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500


@app.route('/getUOM', methods=['GET'])
def get_uom():
    uoms = uom_dao.get_uoms(get_sql_connection())
    response = jsonify(uoms)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(get_sql_connection())
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_playload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(get_sql_connection(),request_playload)
    response = jsonify({
        'product_id' : product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    orders = order_dao.get_all_orders(get_sql_connection())
    response = jsonify(orders)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    try:
        request_payload = json.loads(request.form['data'])
        order_id = order_dao.insert_order(get_sql_connection(), request_payload)
        response = jsonify({'order_id': order_id})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        get_sql_connection().rollback()
        print("ERROR:", e)  
        response = jsonify({
            'error': str(e)
            })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/deleteProducts', methods=['POST'])
def delete_products():
    return_id = products_dao.delete_product(get_sql_connection(), request.form['product_id'])
    response = jsonify({
        'product_id' : return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/searchProducts', methods=['GET'])
def search_products():
    try:
        search_type = request.args.get('search_type')
        search_value = request.args.get('search_value')
        
        if not search_type or not search_value:
            response = jsonify({'error': 'search_type and search_value are required'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        products = products_dao.search_products(get_sql_connection(), search_type, search_value)
        response = jsonify(products)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/searchProductsAdvanced', methods=['GET'])
def search_products_advanced():
    try:
        product_name = request.args.get('product_name')
        product_id = request.args.get('product_id')
        uom_id = request.args.get('uom_id')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        
        products = products_dao.search_products_advanced(
            get_sql_connection(),
            product_name=product_name,
            product_id=product_id,
            uom_id=uom_id,
            min_price=min_price,
            max_price=max_price
        )
        response = jsonify(products)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getOrderById/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        order = order_dao.get_order_by_id(get_sql_connection(), order_id)
        if order:
            response = jsonify(order)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            response = jsonify({'error': 'Order not found'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 404
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/updateOrder/<int:order_id>', methods=['POST'])
def update_order(order_id):
    try:
        request_payload = json.loads(request.form['data'])
        updated_order_id = order_dao.update_order(get_sql_connection(), order_id, request_payload)
        response = jsonify({'order_id': updated_order_id})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        get_sql_connection().rollback()
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500
    
@app.route('/searchOrders', methods=['GET'])
def search_orders():
    try:
        search_type = request.args.get('search_type')
        search_value = request.args.get('search_value')
        
        if not search_type or not search_value:
            response = jsonify({'error': 'search_type and search_value are required'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        orders = order_dao.search_orders(get_sql_connection(), search_type, search_value)
        response = jsonify(orders)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/searchOrdersAdvanced', methods=['GET'])
def search_orders_advanced():
    try:
        customer_name = request.args.get('customer_name')
        order_id = request.args.get('order_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        orders = order_dao.search_orders_advanced(
            get_sql_connection(), 
            customer_name=customer_name, 
            order_id=order_id, 
            start_date=start_date, 
            end_date=end_date
        )
        response = jsonify(orders)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

# ================= INVENTORY ENDPOINTS =================

@app.route('/getInventory', methods=['GET'])
def get_inventory():
    try:
        inventories = inventory_dao.get_all_inventory(get_sql_connection())
        response = jsonify(inventories)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getLowStockItems', methods=['GET'])
def get_low_stock_items():
    try:
        low_stock = inventory_dao.get_low_stock_items(get_sql_connection())
        response = jsonify(low_stock)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/adjustStock', methods=['POST'])
def adjust_stock():
    try:
        request_payload = json.loads(request.form['data'])
        success = inventory_dao.adjust_stock(get_sql_connection(), request_payload)
        
        if success:
            response = jsonify({'success': True, 'message': 'Stock adjusted successfully'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200
        else:
            response = jsonify({'success': False, 'message': 'Failed to adjust stock'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/updateReorderLevels', methods=['POST'])
def update_reorder_levels():
    try:
        request_payload = json.loads(request.form['data'])
        success = inventory_dao.update_reorder_levels(get_sql_connection(), request_payload)
        
        if success:
            response = jsonify({'success': True, 'message': 'Reorder levels updated'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200
        else:
            response = jsonify({'success': False, 'message': 'Failed to update reorder levels'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getStockTransactions', methods=['GET'])
def get_stock_transactions():
    try:
        product_id = request.args.get('product_id')
        transaction_type = request.args.get('transaction_type')
        
        transactions = inventory_dao.get_stock_transactions(
            get_sql_connection(),
            product_id=int(product_id) if product_id else None,
            transaction_type=transaction_type
        )
        
        response = jsonify(transactions)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/searchInventory', methods=['GET'])
def search_inventory():
    try:
        search_type = request.args.get('search_type')
        search_value = request.args.get('search_value')
        
        if not search_type or not search_value:
            response = jsonify({'error': 'search_type and search_value are required'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
        
        inventories = inventory_dao.search_inventory(get_sql_connection(), search_type, search_value)
        response = jsonify(inventories)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500
    
@app.route('/getDashboardStats', methods=['GET'])
def get_dashboard_stats():
    try:
        stats = analytics_dao.get_dashboard_stats(get_sql_connection())
        response = jsonify(stats)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getRevenueTrends', methods=['GET'])
def get_revenue_trends():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        trends = analytics_dao.get_revenue_trends(get_sql_connection(), start_date, end_date)
        response = jsonify(trends)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getTopProducts', methods=['GET'])
def get_top_products():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 10)
        
        products = analytics_dao.get_top_selling_products(
            get_sql_connection(),
            limit=int(limit),
            start_date=start_date,
            end_date=end_date
        )
        response = jsonify(products)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getRevenueByProduct', methods=['GET'])
def get_revenue_by_product():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 10)
        
        products = analytics_dao.get_revenue_by_product(
            get_sql_connection(),
            limit=int(limit),
            start_date=start_date,
            end_date=end_date
        )
        response = jsonify(products)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getMonthlyRevenue', methods=['GET'])
def get_monthly_revenue():
    try:
        months = request.args.get('months', 12)
        
        revenue = analytics_dao.get_monthly_revenue(get_sql_connection(), int(months))
        response = jsonify(revenue)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getCustomerStats', methods=['GET'])
def get_customer_stats():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        customers = analytics_dao.get_customer_statistics(get_sql_connection(), start_date, end_date)
        response = jsonify(customers)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/getInventoryOverview', methods=['GET'])
def get_inventory_overview():
    try:
        overview = analytics_dao.get_inventory_overview(get_sql_connection())
        response = jsonify(overview)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("ERROR:", e)
        response = jsonify({'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500



if __name__ == "__main__":
    print("starting python flask server for grocery store management system")
    app.run(port=5000, debug=True)



    