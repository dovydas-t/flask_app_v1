data = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySqlRootPassword.123',
    'database': 'testdb_register_login_forms_flask',
    'port': 3306
}

def database_url():
    return f"mysql://{data['user']}:{data['password']}@{data['host']}:{data['port']}/{data['database']}"  

# Example usage:
if __name__ == "__main__":
    db_url = database_url()
    print(db_url)  # Output: mysql://root:MySqlRootPassword.123@localhost:3306/testdb_register_login_forms_flask