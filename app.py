from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
import json
import random
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', defaults={'requested_path': 'index.html'})
@app.route('/<path:requested_path>')
def index(requested_path):
    return send_from_directory('build', requested_path)


@app.route('/data')
@cross_origin()
def get_data():
    random_id = random.randint(1, 1000)
    random_support_id = random.randint(1, 1000)
    conn = mysql.connector.connect(
        host="localhost",
        port="8889",
        user="root",
        password="root",
        database="classicmodels"
    )

    cursor = conn.cursor()


# ==selectQuery=================================================================
    selectQuery = "SELECT COUNT(customerNumber) FROM customers;"
    cursor.execute(selectQuery)
# ==============================================================================

    print("***** element count****", cursor.fetchall())

# ==insertQuery=================================================================
#     insertQuery = f"""
# INSERT INTO customers 
#     (customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2,  city, state, postalCode, country, creditLimit, salesRepEmployeeNumber)
# VALUES 
#     ("{random_id}",  "Luis Pérez",         "Pérez",           "Luis", "1234567",   "Xoch",         NULL, "CDMX", "DF",    "12340",    "MX",         "0", NULL); 
# """
    # cursor.execute(insertQuery)
# ==============================================================================

    conn.commit()

    cursor.execute('SELECT contactFirstName, COUNT(contactFirstName) as Count FROM customers GROUP BY contactFirstName ORDER BY Count Desc;')
    data = cursor.fetchall()
    conn.close()
    data_dict = {'FirstName': [row[0] for row in data], 'Count': [row[1] for row in data]}
    print("/data endpoint hit!")
    return jsonify(data_dict)


# @app.route('/', defaults={'requested_path': 'index.html'})
# @app.route('/<path:requested_path>')
# def index(requested_path):
#     return send_from_directory('build', requested_path)


# @app.route('/data')
# @cross_origin()
# def get_data():
#     random_id = random.randint(1, 1000)
#     random_support_id = random.randint(1, 1000)
#     conn = sqlite3.connect('data.db')
#     cursor = conn.cursor()


# # ==selectQuery=================================================================
#     selectQuery = "SELECT COUNT(CustomerId) FROM customers;"
#     cursor.execute(selectQuery)
# # ==============================================================================

#     print("***** element count****", cursor.fetchall())

# # ==insertQuery=================================================================
#     insertQuery = f"""
# INSERT INTO customers 
#     (CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId)
# VALUES 
#     ("{random_id}", "Luis", "Pérez", "Cmpy", "Xoch", "CDMX", "DF", "MX", "12340", "09876543221", "fax123", "email@example.com", "{random_support_id}"); 
# """
#     cursor.execute(insertQuery)
# # ==============================================================================

#     conn.commit()

#     cursor.execute('SELECT FirstName, COUNT(FirstName) as Count FROM customers GROUP BY FirstName ORDER BY Count Desc;')
#     data = cursor.fetchall()
#     conn.close()
#     data_dict = {'FirstName': [row[0] for row in data], 'Count': [row[1] for row in data]}
#     print("/data endpoint hit!")
#     return jsonify(data_dict)



if __name__ == '__main__':
    app.run(port=8000, debug=True)
