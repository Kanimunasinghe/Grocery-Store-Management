def get_uoms(connection):
    cursor = None
    try:
        cursor = connection.cursor()
        query = ("SELECT * FROM uom")
        cursor.execute(query)

        response = []
        for(uom_id, uom_name) in cursor:
            response.append({
                'uom_id': uom_id,
                'uom_name': uom_name
            })
        return response
    
    except Exception as e:
        print("Get UOM error:", e)
        return []
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
    from sql_connection import get_sql_connection
    connection = get_sql_connection()
    print(get_uoms(connection))