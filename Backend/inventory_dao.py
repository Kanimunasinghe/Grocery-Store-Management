from datetime import datetime

def get_all_inventory(connection):
    """Get all inventory with product details"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT i.inventory_id, i.product_id, p.name, p.price_per_unit, u.uom_name, "
                 "i.quantity_on_hand, i.reorder_level, i.reorder_quantity, i.last_updated "
                 "FROM inventory i "
                 "INNER JOIN products p ON i.product_id = p.product_id "
                 "INNER JOIN uom u ON p.uom_id = u.uom_id "
                 "ORDER BY p.name")
        
        cursor.execute(query)
        response = []
        
        for (inventory_id, product_id, name, price, uom_name, qty_on_hand, reorder_level, 
             reorder_qty, last_updated) in cursor:
            status = 'Low Stock' if qty_on_hand <= reorder_level else 'In Stock'
            response.append({
                'inventory_id': inventory_id,
                'product_id': product_id,
                'product_name': name,
                'price_per_unit': float(price) if price else 0,
                'uom_name': uom_name,
                'quantity_on_hand': int(qty_on_hand) if qty_on_hand else 0,
                'reorder_level': int(reorder_level) if reorder_level else 0,
                'reorder_quantity': int(reorder_qty) if reorder_qty else 0,
                'status': status,
                'last_updated': str(last_updated)
            })
        
        return response
    
    except Exception as e:
        print("Get all inventory error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_inventory_by_product(connection, product_id):
    """Get inventory for a specific product"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT i.inventory_id, i.product_id, p.name, p.price_per_unit, u.uom_name, "
                 "i.quantity_on_hand, i.reorder_level, i.reorder_quantity, i.last_updated "
                 "FROM inventory i "
                 "INNER JOIN products p ON i.product_id = p.product_id "
                 "INNER JOIN uom u ON p.uom_id = u.uom_id "
                 "WHERE i.product_id = %s")
        
        cursor.execute(query, (int(product_id),))
        result = cursor.fetchone()
        
        if result:
            (inventory_id, product_id, name, price, uom_name, qty_on_hand, reorder_level, 
             reorder_qty, last_updated) = result
            status = 'Low Stock' if qty_on_hand <= reorder_level else 'In Stock'
            return {
                'inventory_id': inventory_id,
                'product_id': product_id,
                'product_name': name,
                'price_per_unit': float(price) if price else 0,
                'uom_name': uom_name,
                'quantity_on_hand': int(qty_on_hand) if qty_on_hand else 0,
                'reorder_level': int(reorder_level) if reorder_level else 0,
                'reorder_quantity': int(reorder_qty) if reorder_qty else 0,
                'status': status,
                'last_updated': str(last_updated)
            }
        
        return None
    
    except Exception as e:
        print("Get inventory by product error:", e)
        return None
    finally:
        if cursor:
            cursor.close()

def update_quantity(connection, product_id, quantity_change, transaction_type, reference_id=None, notes=None):
    """Update inventory quantity and record transaction"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Update inventory quantity
        update_query = ("UPDATE inventory SET quantity_on_hand = quantity_on_hand + %s "
                       "WHERE product_id = %s")
        cursor.execute(update_query, (float(quantity_change), int(product_id)))
        
        # Record transaction
        transaction_query = ("INSERT INTO stock_transactions "
                           "(product_id, transaction_type, quantity, reference_id, notes) "
                           "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(transaction_query, (int(product_id), transaction_type, float(quantity_change), reference_id, notes))
        
        connection.commit()
        return True
    
    except Exception as e:
        print("Update quantity error:", e)
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def adjust_stock(connection, inventory_adjustment):
    """Manual stock adjustment"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        product_id = int(inventory_adjustment['product_id'])
        adjustment_qty = float(inventory_adjustment['adjustment_quantity'])
        notes = inventory_adjustment.get('notes', 'Manual adjustment')
        
        # Update inventory
        update_query = ("UPDATE inventory SET quantity_on_hand = quantity_on_hand + %s "
                       "WHERE product_id = %s")
        cursor.execute(update_query, (adjustment_qty, product_id))
        
        # Record transaction
        transaction_query = ("INSERT INTO stock_transactions "
                           "(product_id, transaction_type, quantity, notes) "
                           "VALUES (%s, %s, %s, %s)")
        cursor.execute(transaction_query, (product_id, 'adjustment', adjustment_qty, notes))
        
        connection.commit()
        return True
    
    except Exception as e:
        print("Adjust stock error:", e)
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def update_reorder_levels(connection, inventory_update):
    """Update reorder level and quantity"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        update_query = ("UPDATE inventory SET reorder_level = %s, reorder_quantity = %s "
                       "WHERE product_id = %s")
        cursor.execute(update_query, (int(inventory_update['reorder_level']), 
                                     int(inventory_update['reorder_quantity']),
                                     int(inventory_update['product_id'])))
        
        connection.commit()
        return True
    
    except Exception as e:
        print("Update reorder levels error:", e)
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def get_low_stock_items(connection):
    """Get products with low stock (below reorder level)"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT i.inventory_id, i.product_id, p.name, p.price_per_unit, u.uom_name, "
                 "i.quantity_on_hand, i.reorder_level, i.reorder_quantity "
                 "FROM inventory i "
                 "INNER JOIN products p ON i.product_id = p.product_id "
                 "INNER JOIN uom u ON p.uom_id = u.uom_id "
                 "WHERE i.quantity_on_hand <= i.reorder_level "
                 "ORDER BY i.quantity_on_hand ASC")
        
        cursor.execute(query)
        response = []
        
        for row in cursor.fetchall():
            if len(row) >= 8:
                (inventory_id, product_id, name, price, uom_name, qty_on_hand, reorder_level, 
                 reorder_qty) = row[0:8]
                response.append({
                    'inventory_id': inventory_id,
                    'product_id': product_id,
                    'product_name': name,
                    'price_per_unit': float(price) if price else 0,
                    'uom_name': uom_name,
                    'quantity_on_hand': int(qty_on_hand) if qty_on_hand else 0,
                    'reorder_level': int(reorder_level) if reorder_level else 0,
                    'reorder_quantity': int(reorder_qty) if reorder_qty else 0,
                    'shortage': int(reorder_level) - int(qty_on_hand) if qty_on_hand else int(reorder_level)
                })
        
        return response
    
    except Exception as e:
        print("Get low stock items error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def get_stock_transactions(connection, product_id=None, transaction_type=None, limit=100):
    """Get stock transaction history"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = ("SELECT st.transaction_id, st.product_id, p.name, st.transaction_type, "
                 "st.quantity, st.reference_id, st.notes, st.created_at "
                 "FROM stock_transactions st "
                 "INNER JOIN products p ON st.product_id = p.product_id "
                 "WHERE 1=1")
        params = []
        
        if product_id and str(product_id).strip():
            query += " AND st.product_id = %s"
            params.append(int(product_id))
        
        if transaction_type and str(transaction_type).strip():
            query += " AND st.transaction_type = %s"
            params.append(str(transaction_type).strip())
        
        query += " ORDER BY st.created_at DESC LIMIT %s"
        params.append(int(limit))
        
        cursor.execute(query, params)
        response = []
        
        for row in cursor.fetchall():
            if len(row) >= 8:
                (transaction_id, product_id, product_name, trans_type, qty, ref_id, notes, created_at) = row[0:8]
                response.append({
                    'transaction_id': transaction_id,
                    'product_id': product_id,
                    'product_name': product_name,
                    'transaction_type': trans_type,
                    'quantity': float(qty) if qty else 0,
                    'reference_id': ref_id,
                    'notes': notes if notes else '',
                    'created_at': str(created_at)
                })
        
        return response
    
    except Exception as e:
        print("Get stock transactions error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def search_inventory(connection, search_type, search_value):
    """Search inventory by product name or ID"""
    cursor = None
    try:
        cursor = connection.cursor()
        response = []
        
        if search_type == 'product_id':
            query = ("SELECT i.inventory_id, i.product_id, p.name, p.price_per_unit, u.uom_name, "
                     "i.quantity_on_hand, i.reorder_level, i.reorder_quantity, i.last_updated "
                     "FROM inventory i "
                     "INNER JOIN products p ON i.product_id = p.product_id "
                     "INNER JOIN uom u ON p.uom_id = u.uom_id "
                     "WHERE p.product_id = %s")
            cursor.execute(query, (int(search_value),))
        
        elif search_type == 'product_name':
            query = ("SELECT i.inventory_id, i.product_id, p.name, p.price_per_unit, u.uom_name, "
                     "i.quantity_on_hand, i.reorder_level, i.reorder_quantity, i.last_updated "
                     "FROM inventory i "
                     "INNER JOIN products p ON i.product_id = p.product_id "
                     "INNER JOIN uom u ON p.uom_id = u.uom_id "
                     "WHERE LOWER(p.name) LIKE LOWER(%s)")
            cursor.execute(query, (f"%{search_value}%",))
        
        else:
            return response
        
        for row in cursor.fetchall():
            if len(row) >= 9:
                (inventory_id, product_id, name, price, uom_name, qty_on_hand, reorder_level, 
                 reorder_qty, last_updated) = row[0:9]
                status = 'Low Stock' if qty_on_hand <= reorder_level else 'In Stock'
                response.append({
                    'inventory_id': inventory_id,
                    'product_id': product_id,
                    'product_name': name,
                    'price_per_unit': float(price) if price else 0,
                    'uom_name': uom_name,
                    'quantity_on_hand': int(qty_on_hand) if qty_on_hand else 0,
                    'reorder_level': int(reorder_level) if reorder_level else 0,
                    'reorder_quantity': int(reorder_qty) if reorder_qty else 0,
                    'status': status,
                    'last_updated': str(last_updated)
                })
        
        return response
    
    except Exception as e:
        print("Search inventory error:", e)
        return []
    finally:
        if cursor:
            cursor.close()
