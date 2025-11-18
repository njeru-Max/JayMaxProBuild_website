import os
import sqlite3
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory

app = Flask(__name__)

DATABASE = "cart.db"

# Initialize the SQLite database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE cart (
                id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        cursor.executemany("INSERT INTO cart (product_name, quantity, price) VALUES (?, ?, ?)", [
            ("Laptop", 1, 999.99),
            ("Wireless Mouse", 2, 25.50),
            ("Keyboard", 1, 45.75),
            ("Headphones", 1, 79.99)
        ])
        conn.commit()
        conn.close()

# Endpoint to fetch cart items
@app.route('/api/cart')
def get_cart():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, quantity, price FROM cart")
    rows = cursor.fetchall()
    conn.close()
    cart_items = [
        {"productName": row[0], "quantity": row[1], "price": row[2]}
        for row in rows
    ]
    return jsonify(cart_items)

# Endpoint to process checkout
@app.route('/api/checkout', methods=['POST'])
def process_checkout():
    data = request.get_json()
    grand_total = data.get('grandTotal', 0)
    print(f"Processing checkout for total: ${grand_total:.2f}")

    # Clear the cart after checkout
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart")
    conn.commit()
    conn.close()

    return jsonify({"message": "Checkout successful!"}), 200

# Serve the checkout.html file
@app.route('/checkout')
def serve_checkout():
    return send_from_directory(os.getcwd(), 'checkout.html')

# Serve the thankyou.html file
@app.route('/thankyou')
def serve_thankyou():
    return send_from_directory(os.getcwd(), 'thankyou.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
