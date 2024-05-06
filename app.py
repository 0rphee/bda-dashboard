from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
import json
import random
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def exec_query(query: str):
    conn = mysql.connector.connect(
        host="db", port="3306", user="root", password="root", database="steam_db"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


@app.route("/", defaults={"requested_path": "index.html"})
@app.route("/<path:requested_path>")
@cross_origin()
def index(requested_path):
    return send_from_directory("proy-bda-frontend/build", requested_path)


# 1: Gráfica de Barras: porcentaje de los juegos que tienen los developers.
@app.route("/data1")
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
          developer != "" AND
          developer != "nan"
        GROUP BY
          developer
        ORDER BY
          conteo_de_juegos DESC
        LIMIT
          10
    """

    data = exec_query(query)

    data_dict = {
        "Developer": [row[0] for row in data],
        "N_Games": [row[1] for row in data],
    }

    return jsonify(data_dict)


# 2: Gráfica de Barras Porcentaje de los juegos que tienen los publishers.
@app.route("/data2")
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
          publisher != "" AND
          developer != "nan"
        GROUP BY
          publisher
        ORDER BY
          conteo_de_juegos DESC
        LIMIT
          10;
    """

    data = exec_query(query)

    data_dict = {
        "Publisher": [row[0] for row in data],
        "N_Games": [row[1] for row in data],
    }

    return jsonify(data_dict)


# 3: Tabla: Porcentaje de los ratings positivos por juego que más ratings tienen.
@app.route("/data3")
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
        "Developer": [row[0] for row in data],
        "Total_ratings": [row[1] for row in data],
        "Positive_rating_percentage": [row[2] for row in data],
    }

    return jsonify(data_dict)


# 6: Bubble Chart: se entrega el top 100 de juegos con más avg_owners y se les acompaña con la tabla de precio para ver si hay una relación existente entre el precio y la cantidad de usuarios.
@app.route("/data6")
@cross_origin()
def get_data_6():

    query = """
        SELECT appid, name, avg_owners, price, (positive_ratings / (negative_ratings + positive_ratings)) * 100 AS percentage_positive_ragins
        FROM steam
        ORDER BY avg_owners DESC
        LIMIT 100;
    """

    data = exec_query(query)

    data_dict = map(
        lambda row: {
            "appid": row[0],
            "name": row[1],
            "avg_owners": row[2],
            "price": row[3],
            "positive_ratings": row[4],
        },
        data,
    )
    return jsonify(list(data_dict))


# 7: Se seleccionan los juegos con más average playtime y se compara con la cantidad de owners que tiene cada juego
@app.route("/data7")
@cross_origin()
def get_data_7():

    query = """
        SELECT 
            appid,
            name,
            average_playtime,
            avg_owners
        FROM
            steam
        ORDER BY
            average_playtime DESC
        LIMIT 100 
    """

    data = exec_query(query)

    data_dict = map(
        lambda row: {
            "appid": row[0],
            "name": row[1],
            "average_playtime": row[2],
            "avg_owners": row[3],
        },
        data,
    )
    return jsonify(list(data_dict))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


@app.route("/data11")
@cross_origin()
def get_data_11():
    query = """
        SELECT c.Category, c.Category_Count, c.avg_owners_per_cat
        FROM (
            SELECT
                SUBSTRING_INDEX(SUBSTRING_INDEX(categories, ';', numbers.n), ';', -1) AS Category,
                COUNT(*) AS Category_Count,
                AVG(avg_owners) AS avg_owners_per_cat
            FROM
                steam
            JOIN (
                SELECT
                    (a.N + b.N * 10 + 1) AS n
                FROM
                    (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS a
                    CROSS JOIN (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS b
            ) AS numbers ON CHAR_LENGTH(categories) - CHAR_LENGTH(REPLACE(categories, ';', '')) >= numbers.n - 1
            GROUP BY Category
            ORDER BY Category_Count DESC, avg_owners_per_cat DESC
        ) AS c
        WHERE c.Category IN ('Single-player', 'Multi-player', 'Online Multi-Player', 'Shared/Split Screen', 'Co-op', 'Local Multi-Player', 'Cross-Platform Multiplayer', 'Online Co-op', 'Local Co-op')
        LIMIT 4
    """

    data = exec_query(query)

    data_dict = []
    for row in data:
        data_dict.append(
            {"Category": row[0], "Category_Count": row[1], "avg_owners_per_cat": row[2]}
        )

    return jsonify(data_dict)


@app.route("/data12")
@cross_origin()
def get_data_12():
    query = """
        SELECT 
            developer, 
            SUM(CASE WHEN MATCH(genres) AGAINST("Indie")>0 THEN price*avg_owners ELSE 0 END) AS Indie, 
            SUM(CASE WHEN MATCH(genres) AGAINST("Action")>0 THEN price*avg_owners ELSE 0 END) AS ActioN , 
            SUM(CASE WHEN MATCH(genres) AGAINST("Casual")>0 THEN price*avg_owners ELSE 0 END) AS Casual,
            SUM(CASE WHEN MATCH(genres) AGAINST("Adventure")>0 THEN price*avg_owners ELSE 0 END) AS Adventure,
            SUM(CASE WHEN MATCH(genres) AGAINST("Strategy")>0 THEN price*avg_owners ELSE 0 END) AS Strategy,
            SUM(CASE WHEN MATCH(genres) AGAINST("Simulation")>0 THEN price*avg_owners ELSE 0 END) AS Simulation,
            SUM(CASE WHEN MATCH(genres) AGAINST("RPG")>0 THEN price*avg_owners ELSE 0 END) AS RPG,
            SUM(CASE WHEN MATCH(genres) AGAINST("Free to Play")>0 THEN price*avg_owners ELSE 0 END) AS FreePlay,
            SUM(CASE WHEN MATCH(genres) AGAINST("Sports")>0 THEN price*avg_owners ELSE 0 END) AS Sports
        FROM steam 
        WHERE developer IN ("Valve","CAPCOM Co., Ltd.","IO Interactive A/S", "Studio Wildcard;Instinct Games;Efecto Studios;Virtual Basement LLC","Ubisoft Montreal","Bethesda Game Studios","Paradox Development Studio","PUBG Corporation", "Choice of Games")
        GROUP BY developer;
    """

    data = exec_query(query)

    data_dict = []
    for row in data:
        data_dict.append(
            {
                "developer": row[0],
                "Indie": row[1],
                "Act": row[2],
                "Casual": row[3],
                "Adventure": row[4],
                "Strategy": row[5],
                "Simulation": row[6],
                "RPG": row[7],
                "FreePlay": row[8],
                "Sports": row[9],
            }
        )

    return jsonify(data_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
