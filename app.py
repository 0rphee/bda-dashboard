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
    return send_from_directory('proy-bda-frontend/build', requested_path)


@app.route('/data')
@cross_origin()
def get_data():
    random_id = random.randint(1, 1000)
    random_support_id = random.randint(1, 1000)
    conn = mysql.connector.connect(
        # host="localhost",
        # Use the docker-compose service name as the hostname
        host="db",  
        port="3306",
        user="root",
        password="root",
        database="steam_db"
    )

    cursor = conn.cursor()

    # ==selectQuery=================================================================
    # selectQuery = "SELECT COUNT(developer) FROM steam;"
    # cursor.execute(selectQuery)
    # ==============================================================================
    # print("***** element count****", cursor.fetchall())

    cursor.execute('SELECT developer, COUNT(developer) as Count FROM steam WHERE developer != "" GROUP BY developer ORDER BY Count DESC LIMIT 100;')
    data = cursor.fetchall()
    conn.close()
    data_dict = {'Developer': [row[0] for row in data], 'Count': [row[1] for row in data]}
    print("/data endpoint hit!")
    return jsonify(data_dict)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
