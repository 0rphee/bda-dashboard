from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
import json
import random
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def exec_query(query: str):
    conn = mysql.connector.connect(
        host="db",  
        port="3306",
        user="root",
        password="root",
        database="steam_db"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


@app.route('/', defaults={'requested_path': 'index.html'})
@app.route('/<path:requested_path>')
def index(requested_path):
    return send_from_directory('proy-bda-frontend/build', requested_path)


@app.route('/data')
@cross_origin()
def get_data():
    data = exec_query('SELECT developer, COUNT(developer) as Count FROM steam WHERE developer != "" GROUP BY developer ORDER BY Count DESC LIMIT 100;')

    data_dict = {'Developer': [row[0] for row in data], 'Count': [row[1] for row in data]}

    return jsonify(data_dict)

@app.route('/data1')
@cross_origin()
def get_data_1():

    query = """
        WITH TotalJuegos AS (
          SELECT
        	COUNT(*) AS total
          FROM
        	steam
          WHERE
        	developer IS NOT NULL AND
        	developer <> ''
        )
        
        SELECT
          developer,
          COUNT(*) AS conteo_de_juegos,
          (COUNT(*) * 100.0) / (SELECT total FROM TotalJuegos) AS porcentaje
        FROM
          steam
        WHERE
          developer IS NOT NULL AND
          developer <> ''
        GROUP BY
          developer
        ORDER BY
          conteo_de_juegos DESC
        LIMIT
          10
    """

    data = exec_query(query)

    data_dict = {
         'Developer': [row[0] for row in data],
         'N_Games': [row[1] for row in data],
         'P_Steam_games': [row[2] for row in data]
     }

    return jsonify(data_dict)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
