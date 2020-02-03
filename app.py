# app.py
from flask import Flask, request, jsonify
import flask
from flask_cors import CORS, cross_origin
import psycopg2
import random
import string
import traceback
import json
app = Flask(__name__)

@app.route('/checkOrderStatus/', methods=['POST'])
@cross_origin()
def respond():
    # Retrieve the name from url parameter
    try:
        data = json.loads(flask.request.data)
        orderID = data['orderID']
        global conn
        cursor = conn.cursor()
        query = '''SELECT name, items, status FROM public.orders WHERE orderID=%s'''
        cursor.execute(query, (orderID,))
        orderStatus = cursor.fetchone()
        cursor.close()
        return (json.dumps(
            {
                "orderStatus":orderStatus
            }
        ), 200, {'content-type':'application/json'})
    except:
        traceback.print_exc()
        
        
    

@app.route('/addOrder/', methods=['POST'])
@cross_origin()
def post_something():
    try:
        data = json.loads(flask.request.data)
        # args = flask.request.args
        # form = flask.request.form
        status = "Order fulfilled!"
        order = data['pizza'].strip() + " with "+ ', '.join(data['toppings'])
        print(order)
        orderID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # conn = make_conn()
        global conn
        cursor = conn.cursor()
        query = '''INSERT INTO public.orders (orderid, name, phone_no, items, status) VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(query, (orderID, data['name'], data['pno'], order, status))
        conn.commit()
        cursor.close()
        return (json.dumps(
            {   
                "orderID": orderID,
                "message":"Order submitted successfully"
            }
        ), 200, {'content-type': 'application/json'})
    except:
        traceback.print_exc()
    
    

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


def make_conn():
    print("Connecting to database")
    db_name = "xmoduipm"
    db_user = "xmoduipm"
    db_host = "rajje.db.elephantsql.com"
    # db_host = "localhost"
    db_pass = "AVt9GfBQHYXZwVnyrgpV9u781NszT6Cb"
    conn = psycopg2.connect("dbname = '%s' user = '%s' host = '%s' password = '%s'" % (db_name,db_user,db_host,db_pass))
    print("DB connection established")
    return conn

conn = make_conn()

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)