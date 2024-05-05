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
@cross_origin()
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

        SELECT
          developer,
          COUNT(*) AS conteo_de_juegos
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
     }

    return jsonify(data_dict)

@app.route('/data2')
@cross_origin()
def get_data_2():

    query = """
        SELECT
          publisher,
          COUNT(*) AS conteo_de_juegos
        FROM
          steam
        WHERE
          publisher IS NOT NULL AND
          publisher <> ''
        GROUP BY
          publisher
        ORDER BY
          conteo_de_juegos DESC
        LIMIT
          10;
    """

    data = exec_query(query)

    data_dict = {
         'Publisher': [row[0] for row in data],
         'N_Games': [row[1] for row in data],
     }

    return jsonify(data_dict)

@app.route('/data3')
@cross_origin()
def get_data_3():

    query = """

        SELECT developer, SUM(positive_ratings) as Total_Ratings, AVG(positive_ratings / (negative_ratings + positive_ratings)) * 100 AS positive_ratings_percentage
        FROM steam
        WHERE
          (positive_ratings + negative_ratings) > 0
        GROUP BY developer
        ORDER BY Total_Ratings DESC
        LIMIT 10;
    """

    data = exec_query(query)

    data_dict = {
         'Developer': [row[0] for row in data],
         'Total_ratings': [row[1] for row in data],
         'Positive_rating_percentage': [row[2] for row in data],
     }

    return jsonify(data_dict)

@app.route('/data8')
@cross_origin()
def get_data_8():

    query = """
        SELECT appid, name, avg_owners, price, positive_ratings
        FROM steam
        ORDER BY avg_owners DESC
        LIMIT 100;
    """

    data = exec_query(query)

    data_dict = map(lambda row: {"appid": row[0], "name": row[1], "avg_owners": row[2], "price": row[3], "positive_ratings": row[4]}, data)
    return jsonify(list(data_dict))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
