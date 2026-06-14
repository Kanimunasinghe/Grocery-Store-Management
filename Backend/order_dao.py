from datetime import datetime
from sql_connection import get_sql_connection
from datetime import datetime

def insert_order(connection, order):
    cursor = None
    try:
        cursor = connection.cursor()

        order_query = ("INSERT INTO orders "
                 "(customer_name, total, date_time)"
                 "VALUES (%s, %s, %s)")
        order_data = (order['customer_name'], order['total'], datetime.now())

        cursor.execute(order_query, order_data)
        order_id = cursor.lastrowid

        order_details_query = ("INSERT INTO order_details "
                               "(order_id, product_id, quantity, total)"
                               "VALUES (%s, %s, %s, %s)")

        order_details_data = []

        print("order_details received:", order['order_details'])

        for order_detail_record in order['order_details']:
            order_details_data.append([
                order_id,
                int(order_detail_record['product_id']),
                float(order_detail_record['quantity']),
                float(order_detail_record['total_price'])
            ])
            
        cursor.executemany(order_details_query, order_details_data)
        
        # AUTO-REDUCE INVENTORY FOR EACH ITEM IN ORDER
        for order_detail_record in order['order_details']:
            product_id = int(order_detail_record['product_id'])
            quantity = float(order_detail_record['quantity'])
            
            # Update inventory
            inventory_update = ("UPDATE inventory SET quantity_on_hand = quantity_on_hand - %s "
                               "WHERE product_id = %s")
            cursor.execute(inventory_update, (quantity, product_id))
            
            # Record transaction
            transaction_query = ("INSERT INTO stock_transactions "
                               "(product_id, transaction_type, quantity, reference_id, notes) "
                               "VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(transaction_query, (product_id, 'order', -quantity, order_id, 
                                             f'Order #{order_id}'))
        
        connection.commit()
        return order_id
    
    except Exception as e:
        print("Insert order error:", e)
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def get_order_details(connection, order_id):
    cursor = None
    try:
        cursor = connection.cursor()

        query = "SELECT order_details.order_id, order_details.product_id, order_details.quantity, order_details.total, "\
                "products.name, products.price_per_unit FROM order_details LEFT JOIN products on " \
                "order_details.product_id = products.product_id where order_details.order_id = %s "

        data = (order_id, )

        cursor.execute(query, data)

        records = []
        for (order_id, product_id, quantity, total, product_name, price_per_unit) in cursor:
            records.append({
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'total': total,
                'product_name': product_name,
                'price_per_unit': price_per_unit
            })

        return records
    
    except Exception as e:
        print("Get order details error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_all_orders(connection):
    cursor = None
    try:
        cursor = connection.cursor()
        query = ("SELECT * FROM orders")
        cursor.execute(query)
        response = []
        for (order_id, customer_name, total, dt) in cursor:
            response.append({
                'order_id': order_id,
                'customer_name': customer_name,
                'total': total,
                'datetime': str(dt),
            })

        cursor.close()
        cursor = None

        # append order details in each order
        for record in response:
            record['order_details'] = get_order_details(connection, record['order_id'])

        return response
    
    except Exception as e:
        print("Get all orders error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_order_by_id(connection, order_id):
    cursor = None
    try:
        cursor = connection.cursor()

        query = "SELECT order_id, customer_name, total, date_time FROM orders WHERE order_id = %s"
        data = (order_id, )

        cursor.execute(query, data)

        order = None
        for (order_id, customer_name, total, date_time) in cursor:
            order = {
                'order_id': order_id,
                'customer_name': customer_name,
                'total': total,
                'datetime': str(date_time),
                'order_details': get_order_details(connection, order_id)
            }

        return order
    
    except Exception as e:
        print("Get order by id error:", e)
        return None
    finally:
        if cursor:
            cursor.close()

def update_order(connection, order_id, order):
    cursor = None
    try:
        cursor = connection.cursor()

        # STEP 1: Get OLD order details to calculate inventory changes
        old_details_query = ("SELECT product_id, quantity FROM order_details WHERE order_id = %s")
        cursor.execute(old_details_query, (order_id,))
        old_details = {}
        for (product_id, quantity) in cursor:
            old_details[int(product_id)] = float(quantity)

        # STEP 2: Update order header
        order_query = ("UPDATE orders SET "
                       "customer_name = %s, total = %s "
                       "WHERE order_id = %s")
        order_data = (order['customer_name'], order['total'], order_id)
        cursor.execute(order_query, order_data)

        # STEP 3: Delete existing order details
        delete_query = "DELETE FROM order_details WHERE order_id = %s"
        cursor.execute(delete_query, (order_id,))

        # STEP 4: Insert new order details
        order_details_query = ("INSERT INTO order_details "
                               "(order_id, product_id, quantity, total)"
                               "VALUES (%s, %s, %s, %s)")

        order_details_data = []
        new_details = {}

        for order_detail_record in order['order_details']:
            product_id = int(order_detail_record['product_id'])
            quantity = float(order_detail_record['quantity'])
            
            order_details_data.append([
                order_id,
                product_id,
                quantity,
                float(order_detail_record['total_price'])
            ])
            
            new_details[product_id] = quantity

        cursor.executemany(order_details_query, order_details_data)

        # STEP 5: UPDATE INVENTORY - Handle all changes
        
        # Products in both old and new (quantities may have changed)
        for product_id in new_details:
            old_qty = old_details.get(product_id, 0)
            new_qty = new_details[product_id]
            qty_difference = old_qty - new_qty  # Positive = increase inventory, Negative = decrease
            
            if qty_difference != 0:
                # Update inventory
                inventory_update = ("UPDATE inventory SET quantity_on_hand = quantity_on_hand + %s "
                                   "WHERE product_id = %s")
                cursor.execute(inventory_update, (qty_difference, product_id))
                
                # Record transaction
                transaction_query = ("INSERT INTO stock_transactions "
                                   "(product_id, transaction_type, quantity, reference_id, notes) "
                                   "VALUES (%s, %s, %s, %s, %s)")
                
                if qty_difference > 0:
                    notes = f'Order #{order_id} edited - quantity reduced by {qty_difference}'
                else:
                    notes = f'Order #{order_id} edited - quantity increased by {abs(qty_difference)}'
                
                cursor.execute(transaction_query, (product_id, 'order', qty_difference, order_id, notes))

        # Products removed from order (restore inventory)
        for product_id in old_details:
            if product_id not in new_details:
                restored_qty = old_details[product_id]
                
                # Update inventory - add back the quantity
                inventory_update = ("UPDATE inventory SET quantity_on_hand = quantity_on_hand + %s "
                                   "WHERE product_id = %s")
                cursor.execute(inventory_update, (restored_qty, product_id))
                
                # Record transaction
                transaction_query = ("INSERT INTO stock_transactions "
                                   "(product_id, transaction_type, quantity, reference_id, notes) "
                                   "VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(transaction_query, (product_id, 'order', restored_qty, order_id, 
                                                 f'Order #{order_id} edited - product removed'))

        # Products added to order (reduce inventory)
        for product_id in new_details:
            if product_id not in old_details:
                new_qty = new_details[product_id]
                
                # Update inventory - reduce for new product
                inventory_update = ("UPDATE inventory SET quantity_on_hand = quantity_on_hand - %s "
                                   "WHERE product_id = %s")
                cursor.execute(inventory_update, (new_qty, product_id))
                
                # Record transaction
                transaction_query = ("INSERT INTO stock_transactions "
                                   "(product_id, transaction_type, quantity, reference_id, notes) "
                                   "VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(transaction_query, (product_id, 'order', -new_qty, order_id, 
                                                 f'Order #{order_id} edited - product added'))

        connection.commit()
        return order_id
    
    except Exception as e:
        print("Update order error:", e)
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def search_orders(connection, search_type, search_value):
    cursor = None
    try:
        response = []
        cursor = connection.cursor()
        
        if search_type == 'order_id':
            query = "SELECT * FROM orders WHERE order_id = %s"
            cursor.execute(query, (int(search_value),))
        elif search_type == 'customer_name':
            query = "SELECT * FROM orders WHERE LOWER(customer_name) LIKE LOWER(%s)"
            cursor.execute(query, (f"%{search_value}%",))
        elif search_type == 'date':
            query = "SELECT * FROM orders WHERE DATE(date_time) = %s"
            cursor.execute(query, (search_value,))
        else:
            return response
        
        for (order_id, customer_name, total, dt) in cursor:
            response.append({
                'order_id': order_id,
                'customer_name': customer_name,
                'total': total,
                'datetime': str(dt),
            })
        
        # append order details in each order
        for record in response:
            record['order_details'] = get_order_details(connection, record['order_id'])
        
        return response
    
    except Exception as e:
        print("Search orders error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def search_orders_advanced(connection, customer_name=None, order_id=None, start_date=None, end_date=None):
    cursor = None
    try:
        response = []
        cursor = connection.cursor()
        
        query = "SELECT * FROM orders WHERE 1=1"
        params = []
        
        if order_id:
            query += " AND order_id = %s"
            params.append(int(order_id))
        
        if customer_name:
            query += " AND LOWER(customer_name) LIKE LOWER(%s)"
            params.append(f"%{customer_name}%")
        
        if start_date:
            query += " AND DATE(date_time) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(date_time) <= %s"
            params.append(end_date)
        
        query += " ORDER BY date_time DESC"
        
        cursor.execute(query, params)
        
        for (order_id, customer_name, total, dt) in cursor:
            response.append({
                'order_id': order_id,
                'customer_name': customer_name,
                'total': total,
                'datetime': str(dt),
            })
        
        # append order details in each order
        for record in response:
            record['order_details'] = get_order_details(connection, record['order_id'])
        
        return response
    
    except Exception as e:
        print("Advanced search orders error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    print(get_order_details(connection,4))
    print(insert_order(connection, {
        'customer_name': 'dhaval',
         'total': '500',
        'datetime': datetime.now(),
         'order_details': [
             {
                 'product_id': 1,
                 'quantity': 2,
                 'total_price': 50
             },
             {
                 'product_id': 3,
                 'quantity': 1,
                 'total_price': 30
             }
         ]
     }))