from flask import Flask, render_template, request, redirect, session
import re
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE

conn = sqlite3.connect('users.db', check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mobile TEXT,
    password TEXT
)
""")

conn.commit()

# REGISTER

@app.route('/register', methods=['GET', 'POST'])
def register():

    error = ""

    if request.method == 'POST':

        mobile = request.form['mobile']
        password = request.form['password']

        # Strong password check

        if not re.match(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
            password
        ):

            error = "❌ Password is not strong"

            return render_template(
                "register.html",
                error=error
            )

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (mobile, password) VALUES (?, ?)",
            (mobile, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template(
        "register.html",
        error=error
    )

# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = ""

    if request.method == 'POST':

        mobile = request.form['mobile']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE mobile=? AND password=?",
            (mobile, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user'] = mobile

            return redirect('/')

        else:

            error = "❌ Password is incorrect"

    return render_template(
        "login.html",
        error=error
    )

# HOME

@app.route('/')
def home():

    if 'user' not in session:
        return redirect('/login')

    return render_template("home.html")

# CART

@app.route('/cart')
def cart():

    return render_template("cart.html")

# CHECKOUT

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    saved_address = ""

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']

        saved_address = address

        return render_template(
            "checkout.html",
            success=True,
            saved_address=saved_address
        )

    return render_template(
        "checkout.html",
        success=False,
        saved_address=saved_address
    )

# product

@app.route('/product/<name>')
def product(name):

    products = {

        "asian-mens-everest": {
            "title": "Asian Men's Everest",
            "price": "₹1499",
            "image": "1.jpeg",
            "description":
            "Premium Asian sports shoes with stylish design."
        },

        "asian": {
            "title": "Asian Shoes",
            "price": "₹899",
            "image": "2.jpeg",
            "description":
            "Comfortable and affordable casual shoes."
        },

        "puma": {
            "title": "Puma Sport",
            "price": "₹2199",
            "image": "3.jpeg",
            "description":
            "Modern sporty shoes with premium comfort."
        },

        "adidas": {
        "title": "Adidas Ultraboost",
        "price": "₹1499",
        "image": "4.jpeg",
        "description": "High performance shoes with soft cushioning."
    },

    "puma": {
        "title": "Puma RS-X",
        "price": "₹1299",
        "image": "5.jpeg",
        "description": "Modern stylish sneakers for men."
    },

    "reebok": {
        "title": "Reebok Runner",
        "price": "₹1179",
        "image": "6.jpeg",
        "description": "Lightweight running shoes with comfort fit."
    },

    "campus": {
        "title": "Campus OG",
        "price": "₹1049",
        "image": "7.jpeg",
        "description": "Affordable casual shoes for everyday wear."
    },

    "sparx": {
        "title": "Sparx Sports",
        "price": "₹899",
        "image": "8.jpeg",
        "description": "Durable sports shoes with strong grip."
    },

    "woodland": {
        "title": "Woodland Trek",
        "price": "₹1249",
        "image": "9.jpeg",
        "description": "Rugged outdoor trekking shoes."
    },

     "doctor": {
        "title": "Doctor Extra Soft",
        "price": "₹1199",
        "image": "10.jpeg",
        "description": "Running Shoe with Memory Foam Insole & Ultrasoft Outsole."
    },

}


    item = products.get(name)

    return render_template(
        "product.html",
        product=item
    )

# LOGOUT

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# Account

@app.route('/account')
def account():

    return render_template("account.html")

# RUN

if __name__ == '__main__':
    app.run(debug=True)

# Product

@app.route('/product')
def product_home():

    return redirect('/')
