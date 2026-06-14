from werkzeug.security import generate_password_hash, check_password_hash

def signup_admin(connection, admin_data):
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Check if username already exists
        check_query = "SELECT admin_id FROM admin_users WHERE username = %s OR email = %s"
        cursor.execute(check_query, (admin_data['username'], admin_data['email']))
        
        existing = cursor.fetchone()
        if existing:
            return {
                'success': False,
                'message': 'Username or Email already exists'
            }
        
        # Hash the password
        hashed_password = generate_password_hash(admin_data['password'])
        
        # Insert new admin user
        insert_query = ("INSERT INTO admin_users (username, email, password) "
                       "VALUES (%s, %s, %s)")
        insert_data = (admin_data['username'], admin_data['email'], hashed_password)
        
        cursor.execute(insert_query, insert_data)
        connection.commit()
        
        admin_id = cursor.lastrowid
        
        return {
            'success': True,
            'admin_id': admin_id,
            'username': admin_data['username'],
            'message': 'Account created successfully'
        }
    
    except Exception as e:
        print("Signup error:", e)
        connection.rollback()
        return {
            'success': False,
            'message': str(e)
        }
    finally:
        if cursor:
            cursor.close()

def signin_admin(connection, username, password):
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Get admin by username or email
        query = ("SELECT admin_id, username, email, password FROM admin_users "
                "WHERE username = %s OR email = %s")
        cursor.execute(query, (username, username))
        
        result = cursor.fetchone()
        
        if not result:
            return {
                'success': False,
                'message': 'Invalid username/email or password'
            }
        
        admin_id, db_username, email, hashed_password = result
        
        # Check password
        if not check_password_hash(hashed_password, password):
            return {
                'success': False,
                'message': 'Invalid username/email or password'
            }
        
        return {
            'success': True,
            'admin_id': admin_id,
            'username': db_username,
            'email': email,
            'message': 'Login successful'
        }
    
    except Exception as e:
        print("Signin error:", e)
        return {
            'success': False,
            'message': str(e)
        }
    finally:
        if cursor:
            cursor.close()

def get_admin_by_id(connection, admin_id):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "SELECT admin_id, username, email FROM admin_users WHERE admin_id = %s"
        cursor.execute(query, (admin_id,))
        result = cursor.fetchone()
        
        if result:
            admin_id, username, email = result
            return {
                'admin_id': admin_id,
                'username': username,
                'email': email
            }
        
        return None
    
    except Exception as e:
        print("Get admin error:", e)
        return None
    finally:
        if cursor:
            cursor.close()

def get_admin_by_username(connection, username):
    cursor = None
    try:
        cursor = connection.cursor()
        query = "SELECT admin_id, username, email FROM admin_users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result:
            admin_id, username, email = result
            return {
                'admin_id': admin_id,
                'username': username,
                'email': email
            }
        
        return None
    
    except Exception as e:
        print("Get admin error:", e)
        return None
    finally:
        if cursor:
            cursor.close()