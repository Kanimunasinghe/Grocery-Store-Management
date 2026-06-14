import mysql.connector

__cnx = None

def get_sql_connection():
    global __cnx
    
    # Always check if connection is alive
    if __cnx is None:
        print("Opening mysql connection")
        __cnx = mysql.connector.connect(
            user='root',
            password='Kanishka@7788',
            database='gs',
            autocommit=True,
            connection_timeout=10
        )
    else:
        # Test connection, reconnect if dead
        try:
            cursor = __cnx.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        except:
            print("Connection dead, reconnecting...")
            __cnx = mysql.connector.connect(
                user='root',
                password='Kanishka@7788',
                database='gs',
                autocommit=True,
                connection_timeout=10
            )
    
    return __cnx