import sqlite3 as s
from user import User



def connect_db(dbCommand,file_name):
    con = s.connect(file_name)
    cur = con.cursor()
    cur.execute(dbCommand)
    rows = cur.fetchall()
    return rows


def insert_db(dbCommand,file_name):
    con = s.connect(file_name)
    cur = con.cursor()
    cur.execute(dbCommand)
    con.commit()
    con.close


def username_check(username):
    find_user = connect_db(f"SELECT username,email,password FROM users WHERE username='{username}'",'users.db')
    if len(find_user) == 1:
        return User(find_user[0][0],find_user[0][1],find_user[0][1])
    else: 
        return False


def watches(name,discreption,price,banner):
    insert_db(f"INSERT INTO watches VALUES ('{name}','{discreption}','{price}','{banner}')",'watch.db')


def contact_form(message,name,email,subject):
    insert_db(f"INSERT INTO contact VALUES ('{message}','{name}','{email}','{subject}')",'watch.db')


def product_detail_page(product):
    for i in product:
        product_dict = {'id':i[0],'title':i[1],'discription':i[2],'price':i[3]}
        return product_dict


def payment(user,name,card_num,expiry,csv):
    insert_db(f"INSERT INTO payments VALUES ('{user}','{name}','{card_num}','{expiry}','{csv}')", 'watch.db')



def order(user, order_num,total_amt, paid_status):
    insert_db(f"INSERT INTO orders VALUES ('{user}','{order_num}','{total_amt}','{paid_status}')", 'watch.db')



def order_items(order_num,item,qty,price,total):
    insert_db(f"INSERT INTO order_items VALUES ('{order_num}','{item}','{qty}','{price}','{total}')", 'watch.db')


def after_payment_order():
    num = connect_db("SELECT MAX(rowid) FROM orders",'watch.db')
    connect_db(f"UPDATE orders SET paid_status='True' WHERE rowid={num[0][0]}",'watch.db')
    return connect_db(f"SELECT * FROM orders WHERE rowid={num[0][0]}",'watch.db')

