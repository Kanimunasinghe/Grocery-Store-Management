from datetime import datetime, timedelta

def get_dashboard_stats(connection):
    """Get overall dashboard statistics"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        stats = {
            'total_revenue': 0,
            'total_orders': 0,
            'average_order_value': 0,
            'low_stock_count': 0,
            'products_in_stock': 0
        }
        
        # Total Revenue
        revenue_query = "SELECT COALESCE(SUM(total), 0) as total FROM orders"
        cursor.execute(revenue_query)
        result = cursor.fetchone()
        if result:
            stats['total_revenue'] = float(result[0])
        
        # Total Orders
        orders_query = "SELECT COUNT(*) as count FROM orders"
        cursor.execute(orders_query)
        result = cursor.fetchone()
        if result:
            stats['total_orders'] = int(result[0])
        
        # Average Order Value
        if stats['total_orders'] > 0:
            stats['average_order_value'] = round(stats['total_revenue'] / stats['total_orders'], 2)
        
        # Low Stock Count
        low_stock_query = "SELECT COUNT(*) as count FROM inventory WHERE quantity_on_hand <= reorder_level"
        cursor.execute(low_stock_query)
        result = cursor.fetchone()
        if result:
            stats['low_stock_count'] = int(result[0])
        
        # Products in Stock
        in_stock_query = "SELECT COUNT(*) as count FROM inventory WHERE quantity_on_hand > 0"
        cursor.execute(in_stock_query)
        result = cursor.fetchone()
        if result:
            stats['products_in_stock'] = int(result[0])
        
        return stats
    
    except Exception as e:
        print("Get dashboard stats error:", e)
        return None
    finally:
        if cursor:
            cursor.close()

def get_revenue_trends(connection, start_date=None, end_date=None):
    """Get daily revenue trends for line chart"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT DATE(date_time) as order_date, COALESCE(SUM(total), 0) as daily_revenue "
                 "FROM orders WHERE 1=1")
        params = []
        
        if start_date:
            query += " AND DATE(date_time) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(date_time) <= %s"
            params.append(end_date)
        
        query += " GROUP BY DATE(date_time) ORDER BY order_date ASC"
        
        cursor.execute(query, params)
        
        trends = []
        for (order_date, daily_revenue) in cursor:
            trends.append({
                'date': str(order_date),
                'revenue': float(daily_revenue)
            })
        
        return trends
    
    except Exception as e:
        print("Get revenue trends error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_top_selling_products(connection, limit=10, start_date=None, end_date=None):
    """Get top selling products by quantity"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT p.product_id, p.name, SUM(od.quantity) as total_quantity, "
                 "SUM(od.total) as total_revenue, p.price_per_unit "
                 "FROM order_details od "
                 "INNER JOIN products p ON od.product_id = p.product_id "
                 "INNER JOIN orders o ON od.order_id = o.order_id "
                 "WHERE 1=1")
        params = []
        
        if start_date:
            query += " AND DATE(o.date_time) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(o.date_time) <= %s"
            params.append(end_date)
        
        query += " GROUP BY p.product_id, p.name, p.price_per_unit "
        query += " ORDER BY total_quantity DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        
        products = []
        for (product_id, name, qty, revenue, price) in cursor:
            products.append({
                'product_id': product_id,
                'product_name': name,
                'total_quantity': float(qty),
                'total_revenue': float(revenue),
                'price_per_unit': float(price)
            })
        
        return products
    
    except Exception as e:
        print("Get top selling products error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_revenue_by_product(connection, limit=10, start_date=None, end_date=None):
    """Get revenue distribution by product"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT p.product_id, p.name, COALESCE(SUM(od.total), 0) as total_revenue "
                 "FROM products p "
                 "LEFT JOIN order_details od ON p.product_id = od.product_id "
                 "LEFT JOIN orders o ON od.order_id = o.order_id "
                 "WHERE 1=1")
        params = []
        
        if start_date:
            query += " AND DATE(o.date_time) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(o.date_time) <= %s"
            params.append(end_date)
        
        query += " GROUP BY p.product_id, p.name "
        query += " ORDER BY total_revenue DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        
        products = []
        for (product_id, name, revenue) in cursor:
            products.append({
                'product_id': product_id,
                'product_name': name,
                'total_revenue': float(revenue)
            })
        
        return products
    
    except Exception as e:
        print("Get revenue by product error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_order_summary(connection, start_date=None, end_date=None):
    """Get order summary statistics"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        summary = {
            'total_orders': 0,
            'total_revenue': 0,
            'average_order_value': 0,
            'max_order_value': 0,
            'min_order_value': 0
        }
        
        query = ("SELECT COUNT(*) as count, "
                 "COALESCE(SUM(total), 0) as total_revenue, "
                 "COALESCE(MAX(total), 0) as max_value, "
                 "COALESCE(MIN(total), 0) as min_value "
                 "FROM orders WHERE 1=1")
        params = []
        
        if start_date:
            query += " AND DATE(date_time) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(date_time) <= %s"
            params.append(end_date)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        if result:
            summary['total_orders'] = int(result[0])
            summary['total_revenue'] = float(result[1])
            summary['max_order_value'] = float(result[2])
            summary['min_order_value'] = float(result[3])
            
            if summary['total_orders'] > 0:
                summary['average_order_value'] = round(summary['total_revenue'] / summary['total_orders'], 2)
        
        return summary
    
    except Exception as e:
        print("Get order summary error:", e)
        return None
    finally:
        if cursor:
            cursor.close()

def get_inventory_overview(connection):
    """Get inventory status overview"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        overview = {
            'total_products': 0,
            'in_stock': 0,
            'low_stock': 0,
            'out_of_stock': 0,
            'total_stock_value': 0
        }
        
        # Total Products
        total_query = "SELECT COUNT(*) as count FROM inventory"
        cursor.execute(total_query)
        result = cursor.fetchone()
        if result:
            overview['total_products'] = int(result[0])
        
        # In Stock
        in_stock_query = "SELECT COUNT(*) as count FROM inventory WHERE quantity_on_hand > reorder_level"
        cursor.execute(in_stock_query)
        result = cursor.fetchone()
        if result:
            overview['in_stock'] = int(result[0])
        
        # Low Stock
        low_stock_query = ("SELECT COUNT(*) as count FROM inventory "
                          "WHERE quantity_on_hand > 0 AND quantity_on_hand <= reorder_level")
        cursor.execute(low_stock_query)
        result = cursor.fetchone()
        if result:
            overview['low_stock'] = int(result[0])
        
        # Out of Stock
        out_of_stock_query = "SELECT COUNT(*) as count FROM inventory WHERE quantity_on_hand = 0"
        cursor.execute(out_of_stock_query)
        result = cursor.fetchone()
        if result:
            overview['out_of_stock'] = int(result[0])
        
        # Stock Value (Quantity * Price)
        value_query = ("SELECT COALESCE(SUM(i.quantity_on_hand * p.price_per_unit), 0) as stock_value "
                      "FROM inventory i "
                      "INNER JOIN products p ON i.product_id = p.product_id")
        cursor.execute(value_query)
        result = cursor.fetchone()
        if result:
            overview['total_stock_value'] = float(result[0])
        
        return overview
    
    except Exception as e:
        print("Get inventory overview error:", e)
        return None
    finally:
        if cursor:
            cursor.close()

def get_monthly_revenue(connection, months=12):
    """Get monthly revenue for the last N months"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT DATE_FORMAT(date_time, '%Y-%m') as month, "
                 "COALESCE(SUM(total), 0) as monthly_revenue "
                 "FROM orders "
                 "WHERE date_time >= DATE_SUB(NOW(), INTERVAL %s MONTH) "
                 "GROUP BY DATE_FORMAT(date_time, '%Y-%m') "
                 "ORDER BY month ASC")
        
        cursor.execute(query, (months,))
        
        revenue = []
        for (month, monthly_total) in cursor:
            revenue.append({
                'month': month,
                'revenue': float(monthly_total)
            })
        
        return revenue
    
    except Exception as e:
        print("Get monthly revenue error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_customer_statistics(connection, start_date=None, end_date=None):
    """Get customer order statistics"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT customer_name, COUNT(*) as order_count, "
                 "COALESCE(SUM(total), 0) as total_spent, "
                 "COALESCE(AVG(total), 0) as avg_spent "
                 "FROM orders WHERE 1=1")
        params = []
        
        if start_date:
            query += " AND DATE(date_time) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(date_time) <= %s"
            params.append(end_date)
        
        query += " GROUP BY customer_name ORDER BY total_spent DESC LIMIT 20"
        
        cursor.execute(query, params)
        
        customers = []
        for (name, order_count, total_spent, avg_spent) in cursor:
            customers.append({
                'customer_name': name,
                'order_count': int(order_count),
                'total_spent': float(total_spent),
                'avg_spent': float(avg_spent)
            })
        
        return customers
    
    except Exception as e:
        print("Get customer statistics error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_daily_sales_count(connection, start_date=None, end_date=None):
    """Get number of orders per day"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT DATE(date_time) as order_date, COUNT(*) as order_count "
                 "FROM orders WHERE 1=1")
        params = []
        
        if start_date:
            query += " AND DATE(date_time) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(date_time) <= %s"
            params.append(end_date)
        
        query += " GROUP BY DATE(date_time) ORDER BY order_date ASC"
        
        cursor.execute(query, params)
        
        sales = []
        for (order_date, order_count) in cursor:
            sales.append({
                'date': str(order_date),
                'orders': int(order_count)
            })
        
        return sales
    
    except Exception as e:
        print("Get daily sales count error:", e)
        return []
    finally:
        if cursor:
            cursor.close()
