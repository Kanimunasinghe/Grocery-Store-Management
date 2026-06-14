from datetime import datetime


def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT order_id, customer_name, total, date_time "
             "FROM orders ORDER BY date_time DESC;")
    cursor.execute(query)

    response = []
    for (order_id, customer_name, total, date_time) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': date_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return response


def insert_new_order(connection, order):
    cursor = connection.cursor()
    total = order.get('grand_total') or order.get('total')
    order_query = ("INSERT INTO orders (customer_name, total, date_time) "
                   "VALUES (%s, %s, %s);")
    cursor.execute(order_query, (order['customer_name'], total, datetime.now()))
    order_id = cursor.lastrowid

    detail_query = ("INSERT INTO order_details (order_id, product_id, quantity, total) "
                    "VALUES (%s, %s, %s, %s);")
    for item in order['order_details']:
        cursor.execute(detail_query, (
            order_id,
            item['product_id'],
            item['quantity'],
            item['total_price']
        ))

    connection.commit()
    return order_id
