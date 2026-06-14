from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = None
    try:
        cursor = connection.cursor()

        query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
                 "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id;")

        cursor.execute(query)
        response = []

        for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
            response.append({
                'product_id': product_id,
                'name': name,
                'uom_id': uom_id,
                'price_per_unit': price_per_unit,
                'uom_name': uom_name
            })

        return response
    
    except Exception as e:
        print("Get all products error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def insert_new_product(connection, product):
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Insert product
        query = ("insert into products (name,uom_id,price_per_unit) " 
            "values (%s,%s,%s);")
        data = (product['product_name'], product['uom_id'], product['price_per_unit'])
        cursor.execute(query, data)
        
        product_id = cursor.lastrowid
        
        # Auto-create inventory record for new product
        inventory_query = ("INSERT INTO inventory (product_id, quantity_on_hand, reorder_level, reorder_quantity) "
                          "VALUES (%s, 0, 10, 50)")
        cursor.execute(inventory_query, (product_id,))
        
        connection.commit()
        return product_id
    
    except Exception as e:
        print("Insert product error:", e)
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def delete_product(connection, product_id):
    cursor = None
    try:
        cursor = connection.cursor()
        query = ("DELETE FROM products where product_id = %s")
        cursor.execute(query, (product_id,))
        connection.commit()
        return product_id
    
    except Exception as e:
        print("Delete product error:", e)
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def search_products(connection, search_type, search_value):
    cursor = None
    try:
        response = []
        cursor = connection.cursor()
        
        if search_type == 'product_id':
            query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
                     "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id "
                     "WHERE products.product_id = %s")
            cursor.execute(query, (int(search_value),))
        elif search_type == 'product_name':
            query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
                     "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id "
                     "WHERE LOWER(products.name) LIKE LOWER(%s)")
            cursor.execute(query, (f"%{search_value}%",))
        else:
            return response
        
        for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
            response.append({
                'product_id': product_id,
                'name': name,
                'uom_id': uom_id,
                'price_per_unit': price_per_unit,
                'uom_name': uom_name
            })
        
        return response
    
    except Exception as e:
        print("Search products error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

def search_products_advanced(connection, product_name=None, product_id=None, uom_id=None, min_price=None, max_price=None):
    cursor = None
    try:
        response = []
        cursor = connection.cursor()
        
        query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
                 "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id WHERE 1=1")
        params = []
        
        if product_id:
            query += " AND products.product_id = %s"
            params.append(int(product_id))
        
        if product_name:
            query += " AND LOWER(products.name) LIKE LOWER(%s)"
            params.append(f"%{product_name}%")
        
        if uom_id:
            query += " AND products.uom_id = %s"
            params.append(int(uom_id))
        
        if min_price:
            query += " AND products.price_per_unit >= %s"
            params.append(float(min_price))
        
        if max_price:
            query += " AND products.price_per_unit <= %s"
            params.append(float(max_price))
        
        query += " ORDER BY products.name"
        
        cursor.execute(query, params)
        
        for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
            response.append({
                'product_id': product_id,
                'name': name,
                'uom_id': uom_id,
                'price_per_unit': price_per_unit,
                'uom_name': uom_name
            })
        
        return response
    
    except Exception as e:
        print("Advanced search products error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

if __name__=='__main__':
    connection = get_sql_connection()
    print(get_all_products(connection))