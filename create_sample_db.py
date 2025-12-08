import sqlite3

def create_sample_database():
    conn = sqlite3.connect("database/sales.db")
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE customers
                   (
                    id INTEGER PRIMARY KEY, 
                    name TEXT, 
                    email TEXT, 
                    total_spent REAL
                   )
                ''')
    
    cursor.execute("INSERT INTO customers VALUES (1, 'KD', 'KD@email.com', 850.25)")
    cursor.execute("INSERT INTO customers VALUES (2, 'KP', 'KP@email.com', 2170.00)")
    cursor.execute("INSERT INTO customers VALUES (3, 'MS', 'MS@email.com', 185.05)")

    cursor.execute('''
                   CREATE TABLE orders
                   (
                    id INTEGER PRIMARY KEY, 
                    customer_id INTEGER, 
                    product TEXT, 
                    amount REAL
                   )
                ''')
    
    cursor.execute("INSERT INTO orders VALUES (1, 1, 'mousepad', 500.00)")
    cursor.execute("INSERT INTO orders VALUES (2, 1, 'books', 350.25)")
    cursor.execute("INSERT INTO orders VALUES (3, 2, 'laptop sleeve', 770.00)")
    cursor.execute("INSERT INTO orders VALUES (4, 2, 'rain gear', 1400.00)")
    cursor.execute("INSERT INTO orders VALUES (5, 3, 'pen set', 185.05)")

    conn.commit()
    conn.close()
    print("database created")

if __name__ == "__main__":
    create_sample_database()