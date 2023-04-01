from flask import Flask, redirect, render_template, request, url_for, session, render_template_string
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from user import User
from db import connect_db, contact_form, username_check, watches, product_detail_page, payment, order, order_items, after_payment_order
from flask_session import Session
import random


"""********
This specific project was created without a large database, 
because its purpose is to connect to another project which is actually store management
"""


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'VerySecret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@login_manager.user_loader
def load_user(username):
    return username_check(username)



@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Home Page
    """
    new_arrivals = connect_db("SELECT name,price,banner FROM watches WHERE banner='True'",'watch.db')
    return render_template('index.html',new_arrivals=new_arrivals)



@app.route("/search", methods=['GET', 'POST'])
def search_result():
    """
    Search result
    """
    q = request.args.get('q')
    if q:
        products = connect_db(f'SELECT rowid,* FROM watches WHERE name LIKE "{q}"','watch.db')
        return render_template('search.html',products=products)
    return render_template('search.html')



@app.route("/shop") 
def shop():
    """
    Shop page
    """
    products = connect_db("SELECT rowid,* FROM watches",'watch.db')
    high_to_low = connect_db("SELECT rowid,* FROM watches ORDER BY -CAST(price as INTEGER)",'watch.db')
    return render_template('shop.html',products=products, high_to_low=high_to_low)



@app.route("/register", methods=['GET', 'POST'])
def register1():
    """
    Register Page
    """
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        registretion = User(username,email,password).register()
        if registretion == True:
            message = 'User created Go to Login'
    return render_template('register.html',message=message)



@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Login Page
    """
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = username_check(username)
        print(user)
        if user != False:
            login_user(user)
            return redirect('/')
    return render_template('login.html')



@app.route("/logout")
@login_required
def logout():
    """
    Logout
    """
    logout_user()
    return redirect("/")



@app.route("/add-watch", methods=['GET', 'POST'])
def add_watch():
    """
    Add Watch
    """
    message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        discreption = request.form.get('discreption')
        price = request.form.get('price')
        banner = request.form.get('banner')
        watches(name,discreption,price,banner)
        message = 'Added'
    return render_template('addwatch.html',message=message)



@app.route("/shop/<name>", methods=['GET', 'POST'])
def product_detail(name):
    """
    Product page
    """
    product_connect = connect_db(f'SELECT rowid,* FROM watches WHERE name="{name}"','watch.db')
    product = product_detail_page(product_connect)
    return render_template('product_details.html', product=product)



@app.route("/contact", methods=['GET', 'POST'])
def contact():
    """
    Comtacte Page
    """
    message = ''
    if request.method == 'POST':
        messageForm = request.form.get('message')
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        print(messageForm,subject)
        contact_form(messageForm,name,email,subject)
        message = 'Sent'
    return render_template('contact.html',message=message)



@app.route("/about")
def about():
    """
    About page
    """
    return render_template('about.html')



@app.route("/add-to-cart", methods=['GET','POST'])
def add_to_cart():
    """
    Add to cart proces After adding producct to cart
    """
    cart_product = {}
    cart_product[str(request.args.get('id'))] = {
        'title':request.args.get('title'),
        'qty':request.args.get('qty'),
        'price':request.args.get('price'),
    }
    if 'cartdata' in session:
        if str(request.args.get('id')) in session['cartdata']:
            cart_data = session['cartdata']
            cart_data[str(request.args.get('id'))]['qty'] = int(cart_product[str(request.args.get('id'))]['qty'])
            cart_data.update(cart_data)
            session['cartdata'] = cart_data
        else:
            cart_data = session['cartdata']
            cart_data.update(cart_product)
            session['cartdata'] = cart_data
    else:
        session['cartdata'] = cart_product
    print(session['cartdata'])
    return {'data':session['cartdata'],'total_items':len(session['cartdata'])}



@app.route("/cart")
def cart_page():
    """
    Cart page to do change or delete
    """
    if len(session['cartdata']) == 0:
        redirect('/')
    total_price = 0
    for product_id,item in session['cartdata'].items():
        total_price += int(item['qty']) * float(item['price'])
    product_dict = {'cart_data':session['cartdata'],'total_items':len(session['cartdata']),'total_price':total_price}
    product = product_dict['cart_data']
    total_items = product_dict['total_items']
    total_final_price = product_dict['total_price']
    return render_template('cart.html', product=product, total_items=total_items, total_final_price=total_final_price)



@app.route("/update-cart")
def update_cart_item():
    """
    Update cart item from cart page
    """
    p_id = str(request.args.get('id'))
    p_qty = request.args.get('qty')
    if 'cartdata' in session:
        if p_id in session['cartdata']:
            cart_data = session['cartdata']
            cart_data[str(request.args.get('id'))]['qty'] = p_qty
            session['cartdata'] = cart_data
    total_price = 0
    for p_id,item in session['cartdata'].items():
        total_price += int(item['qty']) * float(item['price'])
    product_dict = {'cart_data':session['cartdata'],'total_items':len(session['cartdata']),'total_price':total_price}
    product = product_dict['cart_data']
    total_items = product_dict['total_items']
    total_final_price = product_dict['total_price']
    t = render_template_string("{% extends 'ajax/cart_page.html' %}",product=product,total_items=total_items,total_final_price=total_final_price)
    return {'data':t,'total_items':total_items}



@app.route("/delete-from-cart")
def delete_from_cart():
    """
    Delete cart item from cart page
    """
    p_id = str(request.args.get('id'))
    if 'cartdata' in session:
        if p_id in session['cartdata']:
            cart_data = session['cartdata']
            del session['cartdata'][p_id]
            session['cartdata'] = cart_data
    total_price = 0
    for p_id,item in session['cartdata'].items():
        total_price += int(item['qty']) * float(item['price'])
    product_dict = {'cart_data':session['cartdata'],'total_items':len(session['cartdata']),'total_price':total_price}
    product = product_dict['cart_data']
    total_items = product_dict['total_items']
    total_final_price = product_dict['total_price']
    t = render_template_string("{% extends 'ajax/cart_page.html' %}",product=product,total_items=total_items,total_final_price=total_final_price)
    return {'data':t,'total_items':total_items}



@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    """
    Checkout page * The payment is not secured only at this stage for the test * 
    """
    total_price = 0
    totalPrice = 0
    if 'cartdata' in session:
        for p_id,item in session['cartdata'].items():
            totalPrice += int(item['qty']) * float(item['price'])
        orderNum = random.randint(1000,1000000)
        order(current_user.username,orderNum,totalPrice,False)
    for product_id,item in session['cartdata'].items():
        total_price += int(item['qty']) * float(item['price'])
        order_items(orderNum,item['title'],item['qty'],item['price'],float(item['qty'])*float(item['price']))
    product_dict = {'cart_data':session['cartdata'],'total_items':len(session['cartdata']),'total_price':total_price}
    product = product_dict['cart_data']
    total_items = product_dict['total_items']
    total_final_price = product_dict['total_price']
    return render_template('checkout.html', product=product, total_items=total_items, total_final_price=total_final_price)



@app.route("/account", methods=['GET','POST'])
def acouunt():
    """
    Account Page
    """
    if current_user.is_authenticated:
        user_orders = connect_db(f"SELECT * FROM orders WHERE user='{current_user.username}'", 'watch.db')
        return render_template('account.html',user_orders=user_orders)
    else:
        return redirect('/')



@app.route("/orders", methods=['GET','POST'])
def orders():
    """
    User Orders
    """
    if current_user.is_authenticated:
        cartOrders = connect_db(f"SELECT * FROM orders WHERE user='{current_user.username}'", 'watch.db')
        return render_template('orders.html',cartOrders=cartOrders)
    else:
        return redirect('/')



@app.route("/orders/<idnum>", methods=['GET', 'POST'])
def orders_details(idnum):
    """
    User Order Details
    """
    orderDetails = connect_db(f"SELECT * FROM order_items WHERE order_num='{idnum}'",'watch.db')
    return render_template('orderDetails.html',orderDetails=orderDetails)



@app.route("/payment-done", methods=['GET', 'POST'])
def payment_done():
    """
    After Payment Page
    """
    if request.method == 'POST':
        print('hello')
        order = after_payment_order()
        return render_template('payment_done.html')
    else:
        return 'None'




if __name__ == "__main__":
    app.run(debug=True)